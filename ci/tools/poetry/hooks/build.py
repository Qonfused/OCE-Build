#!/usr/bin/env python3

## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""PEP-517 compliant build hook for poetry-core."""

from functools import partial
from importlib.machinery import SourceFileLoader
from os import makedirs as _makedirs
from re import sub as re_sub
from shutil import copytree as _copytree, rmtree as _rmtree

from typing import Optional, Tuple

#pragma preserve-imports - Inject project namespaces into the module search path
import sys, pathlib; sys.path.insert(1, str(pathlib.Path(__file__, '../' * 5).resolve()))

from ci.constants import PROJECT_ROOT, PROJECT_BUILD_STAGING
from ci.constants import _enumerate_modules, IS_FULL_ENV, HAS_RAN_HOOKS

from third_party.cpython.pathlib import Path


# Ensure that filesystem operations are graceful
makedirs = partial(_makedirs, exist_ok=True)
rmtree = partial(_rmtree, ignore_errors=True)
copytree = partial(_copytree, dirs_exist_ok=True)

def replace_module(module: str, replacement: str, string: str) -> str:
  """Replace a module import with a new module import."""
  pattern = r'\n(\s*?)(import|from)\s*' + module + r'\b'
  repl = r'\n\1\2 ' + replacement

  # Add a notice if the namespace is separated for clarity
  notice = f"\n#NOTE: This import was remapped from '{module}' to '{replacement}'."
  string = re_sub(r'\n' + pattern, r'\n' + notice + repl, string)

  return re_sub(pattern, repl, string)

def remap_module_imports(entrypoint: str, mappings: Tuple[str, str]) -> None:
  """Recursively remap module imports in a package."""

  for package in Path(entrypoint).glob('**/*.py'):
    with open(package, 'r', encoding='UTF-8') as module_file:
      file_text = module_file.read()

    # Replace the imports block with the remapped imports
    with open(package, 'w', encoding='UTF-8') as module_file:
      remapped_text = file_text
      for module, replacement in mappings:
        remapped_text = replace_module(module, replacement, remapped_text)
      # Write the updated file back to disk
      module_file.seek(0)
      module_file.write(remapped_text)


def clean(stage: Optional[str]=None):
  """Cleanup the staging directory."""
  if stage != 'post_build': rmtree('dist')
  for target in _enumerate_modules(PROJECT_BUILD_STAGING):
    target_path = f'{PROJECT_BUILD_STAGING}/{target}'
    rmtree(target_path)
    makedirs(target_path)
    open(f'{target_path}/__init__.py', 'w').close()

def _main():
  PROJECT_BUILD_DIR = Path(PROJECT_ROOT, 'ci/tools/poetry/build')
  # Cleanup the build directory
  rmtree(PROJECT_BUILD_DIR)
  makedirs(PROJECT_BUILD_DIR)

  copytree('ocebuild',      f'{PROJECT_BUILD_DIR}/ocebuild')
  copytree('ocebuild_cli',  f'{PROJECT_BUILD_DIR}/ocebuild/cli')
  copytree('third_party',   f'{PROJECT_BUILD_DIR}/ocebuild/third_party')

  # Update module imports
  remap_module_imports(f'{PROJECT_BUILD_DIR}/ocebuild',
                        mappings=(('ocebuild_cli', 'ocebuild.cli'),
                                  ('third_party',  'ocebuild.third_party')))

  # Copy the CLI and third-party packages if not developing the project locally
  if HAS_RAN_HOOKS or not IS_FULL_ENV:
    target = f'{PROJECT_BUILD_DIR}/ocebuild'
  # Otherwise, only copy the project source
  else:
    target = f'{PROJECT_ROOT}/ocebuild'
  copytree(target, f'{PROJECT_BUILD_STAGING}/ocebuild')

if __name__ == '__main__':
  _main()

  if not HAS_RAN_HOOKS:
    # Cleanup the staging directory if pre/post hooks were not triggered
    clean()
    # Ensure the install hook is ran if in a full environment
    if IS_FULL_ENV:
      install_hook = str(Path(PROJECT_ROOT, 'ci/tools/poetry/hooks/install.py'))
      install = SourceFileLoader('install_hook', install_hook).load_module()
      install._main()
