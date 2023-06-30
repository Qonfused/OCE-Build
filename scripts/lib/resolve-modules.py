#!/usr/bin/env python3

## @file
# Regenerates implicit package-level module imports.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

from typing import List

from ocebuild.filesystem.posix import glob
from ocebuild.sources.resolver import PathResolver
from ocebuild import __file__

from _lib import PROJECT_ROOT, PROJECT_ENTRYPOINT


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

if __name__ == '__main__':
  for package in recurse_packages(PROJECT_ENTRYPOINT):
    # Get parent tree/namespace
    ptree = package.relative_to(PROJECT_ROOT).parents[1].__str__()
    if ptree == '.': ptree = ''
    else: ptree += '.'
    # Filter package file SPDX headers
    lines: List[str] = []
    with open(package, 'r', encoding='UTF-8') as init_file:
      for raw_line in init_file.readlines():
        line = raw_line.strip('\n')
        if not line.startswith('#') or not len(line):
          continue
        if line.startswith('#pragma') and 'no-implicit' in line:
          lines = []; break
        lines.append(line)
    # Validate filtered output
    if not len(lines): continue
    else: lines.append('') # Add linebreak
    # Add implicit package imports
    for module in recurse_modules(package.parent):
      lines.append(f'from {ptree}{".".join(module.split("/"))} import *')
    # Update package file
    with open(package, 'w', encoding='UTF-8') as init_file:
      for idx, line in enumerate(lines):
        if idx + 1 < len(lines):
          init_file.write(f"{line}\n")
        else:
          init_file.write(f"{line}")
