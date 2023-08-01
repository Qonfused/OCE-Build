## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""PEP-517 compliant build hook for poetry-core."""

from functools import partial
from os import listdir, makedirs, path
from pathlib import Path
from re import sub as re_sub
from shutil import copytree as _copytree, rmtree as _rmtree

from typing import Tuple


STAGING_PATH = 'ci/tools/poetry/staging'
TARGET = f'{STAGING_PATH}/ocebuild'

# Ensure that filesystem operations are graceful
rmtree = partial(_rmtree, ignore_errors=True)
copytree = partial(_copytree, dirs_exist_ok=True)

def clean():
  """Cleanup the staging directory."""
  for target in filter(path.isdir, listdir(STAGING_PATH)):
    target_path = f'{STAGING_PATH}/{target}'
    rmtree(target_path)
    makedirs(target_path, exist_ok=True)
    open(f'{target_path}/__init__.py', 'w').close()

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


def pre_build():
  clean()

def post_build():
  clean()
  #TODO: Add post-build verification step
  # e.g. inspecting the contents of the sdist/wheel archives:
  # $ python3 -m tarfile -l dist/ocebuild-0.0.0.dev0.tar.gz
  # $ python3 -m zipfile -l dist/ocebuild-0.0.0.dev0-cp311-cp311-macosx_13_0_x86_64.whl

if __name__ == '__main__':
  copytree('ocebuild',      f'{STAGING_PATH}/ocebuild')
  copytree('ocebuild_cli',  f'{STAGING_PATH}/ocebuild/cli')
  copytree('third_party',   f'{STAGING_PATH}/ocebuild/third_party')

  # Update module imports
  remap_module_imports(f'{STAGING_PATH}/ocebuild',
                       mappings=(('ocebuild_cli', 'ocebuild.cli'),
                                 ('third_party',  'ocebuild.third_party')))
