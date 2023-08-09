#!/usr/bin/env python3

## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Sorts import statements within python modules."""

from itertools import groupby
from operator import itemgetter
from os import path as os_path
from re import sub as re_sub

from typing import List, Optional, Union

from ci import PROJECT_BUILD_PATHS, PROJECT_NAMESPACES, PROJECT_ROOT, PYTHON_MODULES

from ocebuild.filesystem import glob
from ocebuild.parsers.regex import re_search

from third_party.cpython.pathlib import Path


PRAGMA_FLAGS = [
  # Skips sorting of import statements
  'preserve-imports',
]
"""Flags to control module imports generation."""

RE_PRAGMA_FLAGS = r'#\s*?pragma\s+(?:{})'.format('|'.join(PRAGMA_FLAGS))

RE_IMPORT_BLOCK = r'(?s)(\n*^(?:from|import).*^(?:from|import).*?\n*$)'
"""Regular expression that matches import statements and adjacent newlines."""

def module_name(s: str) -> str:
  """Returns the root module name of an import statement.

  Examples:
    >>> package_name('import os')
    # -> 'os'
    >>> package_name('from os import path')
    # -> 'os'
    >>> package_name('from os.path import join')
    # -> 'os.path'
  """
  if s.lower().startswith('import'):
    return re_search(r'^import (.*)', s, group=1)
  return re_search(r'^from (.*?) import ', s, group=1)

def package_name(s: str) -> str:
  """Returns the root package name of an import statement.

  Examples:
    >>> package_name('import os')
    # -> 'os'
    >>> package_name('from os import path')
    # -> 'os'
    >>> package_name('from os.path import join')
    # -> 'os'
  """
  return module_name(s).split('.')[0]

def sorting_rules(s: str) -> int:
  """Returns an integer sum of sorting rules for an import statement.

  The sorting rules are as follows:
    - Internal Python packages (e.g. __future__)
    - Native Python packages (e.g. os, sys)
    - Typing packages (e.g. typing, typing_extensions)
    - External Python packages (e.g. numpy, scipy)
    - Project namespace/packages (e.g. ci, ocebuild)

  This is constructed using the following bit flags:
    0: Package is an internal python module.
    1: Package is a native python module.
    2: Package is a typing module
    4: Package is an external python module.
    8: Package is a project namespace/module.
  """
  return (
    (1 * int(not package_name(s).startswith('__'))) +
    (2 * int(any([package_name(s) in (
        'types', 'typing', 'typing_extensions')]))) +
    (4 * int(not package_name(s) in PYTHON_MODULES)) +
    (8 * int(os_path.isdir(
        PROJECT_ROOT.joinpath(package_name(s)))))
  )

def sort_imports_block(imports_block: str) -> str:
  """Sorts import statements in a block of text."""

  # Sort import statements.
  import_statements = re_sub('\n{2,}', '\n', imports_block.strip()).split('\n')
  import_statements = sorted(import_statements,
                             key=lambda s: (
                               # 1: Sort import statements by loader type.
                               0 if s.lower().startswith('import') else 1,
                               # 2: Sort imported packages alphabetically.
                               package_name(s),
                               # 3: Sort imported modules alphabetically.
                               module_name(s),
                             ))

  # Sort modules within import statements.
  for i,s in enumerate(import_statements):
    if s.lower().startswith('import'): continue
    modules = set(map(lambda s: s.strip(),
                  re_sub('^from .*? import ', '', s).split(',')))
    # Sort modules alphabetically.
    modules = sorted(modules,
                     key=lambda s: (s.isupper(),
                                    s.lower().split(' as ')[0],
                                    len(s)))
    # Replace import statement with sorted modules.
    import_statements[i] = f'from {module_name(s)} import {", ".join(modules)}'

  # Group import statements by source.
  import_groups = list(map(lambda s: (s,sorting_rules(s)), import_statements))
  import_groups.sort(key = itemgetter(1))

  # Reconstruct a sorted imports block.
  sorted_block = '\n\n'
  for b,g in groupby(import_groups, key=itemgetter(1)):
    # Separate project namespace/package imports.
    if b >= 8:
      groups_by_namespace = list(map(lambda s: (s[0], package_name(s[0])), g))
      groups_by_namespace.sort(key=itemgetter(1))
      for _,n in groupby(groups_by_namespace, key=itemgetter(1)):
        sorted_block += "\n".join(map(itemgetter(0), n)) + '\n\n'
    # Separate native python modules from external modules and types.
    else:
      sorted_block += "\n".join(map(itemgetter(0), g)) + '\n\n'

  return sorted_block

def sort_file_imports(file: str) -> str:
  """Sorts import statements within file text."""

  pragma_flags = re_search(RE_PRAGMA_FLAGS, file, multiline=True)
  if pragma_flags and 'preserve-imports' in pragma_flags:
    return file

  imports_block = re_search(RE_IMPORT_BLOCK, file, multiline=True)
  if imports_block:
    try:
      sorted_block = sort_imports_block(imports_block)
      return file.replace(imports_block, sorted_block)
    except Exception:
      pass

  return file

def recurse_modules(entrypoint: Union[str, Path]) -> List[str]:
  """Returns a list of all project packages recursively."""
  patterns = map(lambda f: Path(f).resolve(),
                 glob(entrypoint,
                      pattern='**/*.py',
                      exclude='**/__init__.py'))

  packages = sorted(patterns)
  return packages


def _main(entrypoint: Optional[str]=None) -> None:
  # Extract project entrypoint or default to project entrypoint
  if entrypoint:
    entrypoint = PROJECT_ROOT.joinpath(entrypoint)
  if not entrypoint:
    for namespace in PROJECT_NAMESPACES:
      _main(namespace)
    return None

  # Enumerate each package
  for package in recurse_modules(entrypoint):
    if any(str(package).startswith(str(p)) for p in PROJECT_BUILD_PATHS):
      continue
    with open(package, 'r', encoding='UTF-8') as module_file:
      file_text = module_file.read()
      # Sort imports by type
      file_text = sort_file_imports(file_text)
      # Write to file
    Path(package).write_text(file_text, encoding='UTF-8', newline='\n')


__all__ = [
  # Constants (3)
  "PRAGMA_FLAGS",
  "RE_PRAGMA_FLAGS",
  "RE_IMPORT_BLOCK",
  # Functions (6)
  "module_name",
  "package_name",
  "sorting_rules",
  "sort_imports_block",
  "sort_file_imports",
  "recurse_modules"
]
