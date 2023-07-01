#!/usr/bin/env python3

## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Regenerates implicit namespace and package-level module exports.."""

from importlib import import_module
from inspect import getdoc

from typing import List

from ocebuild.filesystem.posix import glob
from ocebuild.parsers.regex import re_search
from ocebuild.sources.resolver import PathResolver
from ocebuild import __file__

from ci import PROJECT_ROOT, PROJECT_ENTRYPOINT


PRAGMA_FLAGS = [
  # Skips creating implicit module exports (`from module.submodule import *``)
  'no-implicit',
  # Skips creatiing explicit public API exports (`__all__ = ["foo", "bar"]`)
  'preserve-exports'
]
"""Flags to control module export generation."""

def recurse_packages(entrypoint: str) -> List[str]:
  """Returns a list of all project packages recursively."""
  patterns = map(lambda f: PathResolver(f).resolve(),
                 glob(entrypoint, pattern='**/__init__.py'))

  packages = sorted(patterns)
  return packages

def recurse_modules(entrypoint: str) -> List[str]:
  """Returns a list of all project modules recursively."""
  patterns = map(lambda f: PathResolver(f).relative(entrypoint),
                 glob(entrypoint,
                      pattern='[!_]*.py',
                      exclude='*_test.py'))

  modules = sorted(map(lambda m: m[:-len('.py')], patterns))
  return modules

def get_public_exports(module_path: str) -> List[str]:
  """Returns a list of public API exports from a module."""
  module = import_module(module_path)
  exports: List[str] = []
  for s in module.__dir__():
    # Skip explicitly marked internals
    if s.startswith('_'): continue
    # Remove external module imports
    export = module.__getattribute__(s)
    try: assert export.__module__ == module_path
    except: continue
    # Skip exports marked as internal
    if (docstring := getdoc(export)):
      internal_annotations = ('@internal', '@private')
      if any(docstring.startswith(a) for a in internal_annotations): continue
    # Otherwise, add to exports
    exports.append(s)
  return exports


def _main():
  # Enumerate each package
  for package in recurse_packages(PROJECT_ENTRYPOINT):
    # Get parent tree/namespace
    ptree = PathResolver(package).relative_to(PROJECT_ROOT).parents[1].__str__()
    if ptree == '.': ptree = ''
    else: ptree += '.'

    # Filter package file SPDX headers
    lines: List[str] = []
    with open(package, 'r', encoding='UTF-8') as init_file:
      for raw_line in init_file.readlines():
        line = raw_line.strip('\n')
        # Handle preprocessor flags
        if line.startswith('#pragma'):
          if 'no-implicit' in line:
            lines = []; break
        # Preserve root comments and docstrings
        if not line.startswith('#') and not line.startswith('"""'):
          continue
        lines.append(line)
    # Validate filtered output
    if not len(lines): continue
    else: lines.append('') # Add linebreak

    # Enumerate each module in the package
    for tree in recurse_modules(package.parent):
      # Add implicit package imports
      module_path = f'{ptree}{".".join(tree.split("/"))}'
      lines.append(f'from {module_path} import *')
      # Add explicit public API exports
      module_exports = get_public_exports(module_path)
      filepath = f'{package.parents[1].joinpath(tree)}.py'
      with open(filepath, 'r', encoding='UTF-8') as module_file:
        file_text = module_file.read()
        # Handle preprocessor flags
        preprocessor_flags = re_search(r'\#pragma\s?(.*)$', file_text,
                                       group=1,
                                       multiline=True)
        if preprocessor_flags:
          if 'preserve-exports' in preprocessor_flags: continue
        # Extract `__all__` exports line
        public_exports = re_search(r'(?s)^__all__ = \[(.*?)\]$', file_text,
                                   multiline=True)
        # Replace text
        replacement_entries = ',\n'.join(map(lambda e: f'  "{e}"',
                                             module_exports))
        replacement_text = f'__all__ = [\n{replacement_entries}\n]'
        if public_exports:
          file_text = file_text.replace(public_exports, replacement_text)
        else:
          file_text += f'\n{replacement_text}\n'
        # Write to file
        PathResolver(filepath).write_text(file_text, encoding='UTF-8')

    # Update package file
    file_text = '\n'.join(lines)
    PathResolver(package).write_text(file_text, encoding='UTF-8')


if __name__ == '__main__':
  _main()
