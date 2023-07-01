#!/usr/bin/env python3

## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Regenerates implicit namespace and package-level module exports.."""

from argparse import ArgumentParser
from ast import parse
from ast import Import, ImportFrom
from ast import Assign, FunctionDef, AsyncFunctionDef, ClassDef
from importlib import import_module
from inspect import getdoc

from typing import List, Optional, Union

from ocebuild.filesystem.posix import glob
from ocebuild.parsers.regex import re_search
from ocebuild.sources.resolver import PathResolver

from ci import PROJECT_ROOT, PROJECT_ENTRYPOINT


PRAGMA_FLAGS = [
  # Skips creating implicit module exports (`from module.submodule import *``)
  'no-implicit',
  # Skips creating explicit public API exports (`__all__ = ["foo", "bar"]`)
  'preserve-exports'
]
"""Flags to control module export generation."""

AST_TYPES_IMPORTS = [
  Import,
  ImportFrom
]
"""Types of AST nodes that represent imports."""

AST_TYPES_STMTS = [
  Assign,
  FunctionDef,
  AsyncFunctionDef,
  ClassDef
]
"""Types of AST nodes that represent statements."""

def _get_parent_tree(package: Union[str, PathResolver]) -> str:
  """Returns the parent tree of a package."""
  ptree = PathResolver(package).relative_to(PROJECT_ROOT).parents[1].__str__()
  if ptree == '.': ptree = ''
  else: ptree += '.'
  return ptree

def recurse_packages(entrypoint: Union[str, PathResolver]) -> List[str]:
  """Returns a list of all project packages recursively."""
  patterns = map(lambda f: PathResolver(f).resolve(),
                 glob(entrypoint, pattern='**/__init__.py'))

  packages = sorted(patterns)
  return packages

def recurse_modules(entrypoint: Union[str, PathResolver]) -> List[str]:
  """Returns a list of all project modules recursively."""
  patterns = map(lambda f: PathResolver(f).relative(entrypoint),
                 glob(entrypoint,
                      pattern='[!_]*.py',
                      exclude='*_test.py'))

  modules = sorted(map(lambda m: m[:-len('.py')], patterns))
  return modules

def get_local_statements(filepath: Union[str, PathResolver]) -> List[str]:
  """Returns a list of local statements from a file."""
  is_import = lambda n: any([ isinstance(n, t) for t in AST_TYPES_IMPORTS ])
  is_def = lambda n: any([ isinstance(n, t) for t in AST_TYPES_STMTS ])

  names: List[str]=[]
  body = parse(open(filepath, 'r').read()).body
  local_stmts = [n for n in body if is_def(n) and not is_import(n)]
  for s in local_stmts:
    if isinstance(s, Assign): names += list(map(lambda n: n.id, s.targets))
    else: names.append(s.name)

  return names

def get_variable_docstring(statement: str,
                           filepath: Union[str, PathResolver]
                           ) -> Union[str, None]:
  with open(filepath, 'r', encoding='UTF-8') as module_file:
    file_text = module_file.read()
    docstring = re_search(f'(?s)^{statement}\s?.*?\n^"""(.*?)"""$', file_text,
                          group=1,
                          multiline=True)
    return docstring

def get_public_exports(filepath: Union[str, PathResolver],
                       module_path: str
                       ) -> List[str]:
  """Returns a list of public API exports from a module."""
  module = import_module(module_path)
  statements = get_local_statements(filepath)
  exports: List[str] = []
  for s in module.__dir__():
    # Remove external module imports
    export = module.__getattribute__(s)
    if hasattr(export, '__loader__'): continue
    try: assert export.__module__ == module_path
    except AssertionError:
      if s not in statements: continue
    except AttributeError: pass

    # Parse docstrings for annotation markers
    docstring = get_variable_docstring(s, filepath)
    if not docstring: docstring = getdoc(export)

    # Skip exports explicitly marked as internal
    internal_annotations = ('@internal', '@private')
    if docstring and any(a in docstring for a in internal_annotations): continue

    # Include explicitly marked externals
    external_annotations = ('@external', '@public')
    if docstring and any(a in docstring for a in external_annotations): pass
    # Skip implicitly marked internals
    elif s.startswith('_'): continue

    # Otherwise, add to exports
    exports.append(s)
  
  return exports

def get_file_header(filepath: Union[str, PathResolver]):
  """Retrieves the file header from a file."""
  lines: List[str] = []
  with open(filepath, 'r', encoding='UTF-8') as init_file:
    has_pragma_line = False
    is_spdx_header = False
    is_docstring = False
    for raw_line in init_file.readlines():
      line = raw_line.strip('\n')
      # Mark and preserve SPDX headers
      if not is_spdx_header and line.startswith('## @file'):
        is_spdx_header = True
      elif is_spdx_header and line.startswith('#'): pass
      # Handle additional inclusions
      else:
        is_spdx_header = False
        # Preserve module docstrings
        if not is_docstring and line.startswith('"""'):
          # Only mark multi-line docstrings
          if not line.endswith('""""') or line.rstrip() == '"""':
            is_docstring = True
        elif is_docstring and line.endswith('"""'):
          is_docstring = False
        # Preserve preprocessor flags
        elif not has_pragma_line and line.startswith('#pragma'):
          has_pragma_line = True
        # Preserve header linebreaks
        elif not len(line): pass
        # Skip all other lines
        elif not all([is_spdx_header, is_docstring]):
          break
        else:
          continue
      lines.append(line)
  return lines

def generate_api_exports(filepath: Union[str, PathResolver],
                         module_path: str
                         ) -> None:
  """Generates a module's API exports."""
  module_exports = get_public_exports(filepath, module_path)
  with open(filepath, 'r', encoding='UTF-8') as module_file:
    file_text = module_file.read()
    # Handle preprocessor flags
    preprocessor_flags = re_search(r'\#pragma\s?(.*)$', file_text,
                                    group=1,
                                    multiline=True)
    if preprocessor_flags:
      if 'preserve-exports' in preprocessor_flags: return
    # Extract `__all__` exports line
    public_exports = re_search(r'(?s)^__all__ = \[(.*?)\]$', file_text,
                                multiline=True)
    # Generate replacement text
    replacement_entries = ',\n'.join(map(lambda e: f'  "{e}"',
                                         module_exports))
    replacement_text = f'__all__ = [\n{replacement_entries}\n]'
    if not len(replacement_entries):
      replacement_text = '__all__ = []'
    # Replace text
    if public_exports:
      file_text = file_text.replace(public_exports, replacement_text)
    else:
      file_text += f'\n{replacement_text}\n'
    # Write to file
    PathResolver(filepath).write_text(file_text, encoding='UTF-8')


def _main(entrypoint: Optional[str]=None
          ) -> None:
  
  # Extract project entrypoint or default to project entrypoint
  if entrypoint: entrypoint = PROJECT_ROOT.joinpath(entrypoint)
  if not entrypoint: entrypoint = PROJECT_ENTRYPOINT

  # Enumerate each package
  for package in recurse_packages(entrypoint):
    # Get parent tree/namespace
    ptree = _get_parent_tree(package)

    # Filter package file SPDX headers
    package_lines = get_file_header(package)
    if not len(package_lines): continue
    pragma_line = package_lines[0] if '#pragma' in package_lines[0] else ''

    # Enumerate each module in the package
    for tree in recurse_modules(package.parent):
      # Add implicit package imports
      module_path = f'{ptree}{".".join(tree.split("/"))}'
      package_lines.append(f'from {module_path} import *')
      # Add explicit public API exports
      filepath = f'{package.parents[1].joinpath(tree)}.py'
      generate_api_exports(filepath, module_path)

    # Update package file
    if not 'no-implicit' in pragma_line:
      package_text = '\n'.join(package_lines)
      PathResolver(package).write_text(package_text, encoding='UTF-8')


if __name__ == '__main__':
  parser = ArgumentParser()
  parser.add_argument(["--entrypoint"],
                      dest='entrypoint',
                      help='The entrypoint to resolve modules for.')
  args = parser.parse_args()

  _main(entrypoint=args.entrypoint)

__all__ = [
  "PRAGMA_FLAGS",
  "AST_TYPES_IMPORTS",
  "AST_TYPES_STMTS",
  "recurse_packages",
  "recurse_modules",
  "get_local_statements",
  "get_variable_docstring",
  "get_public_exports",
  "get_file_header",
  "generate_api_exports"
]
