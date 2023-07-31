## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""PEP-517 compliant build hook for poetry-core."""

from functools import partial
from os import listdir, makedirs, path
from pathlib import Path
from re import search as re_search, sub as re_sub, MULTILINE
from shutil import copytree as _copytree, rmtree as _rmtree

from typing import Tuple


#NOTE: Keep in sync with ci/scripts/sort-imports.py
RE_IMPORT_BLOCK = r'(?s)(\n*^(?:from|import).*^(?:from|import).*?\n*$)'
"""Regular expression that matches import statements and adjacent newlines."""

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
  pattern = r'\n(import|from)\s*' + module + r'\b'
  repl = r'\n\1 ' + replacement

  # Add a notice if the namespace is separated for clarity
  notice = f"\n#NOTE: This import was remapped from '{module}' to '{replacement}'."
  string = re_sub(r'\n' + pattern, r'\n' + notice + repl, string)

  return re_sub(pattern, repl, string)

def remap_module_imports(entrypoint: str, mappings: Tuple[str, str]) -> None:
  """Recursively remap module imports in a package."""

  for package in Path(entrypoint).glob('**/*.py'):
    with open(package, 'r', encoding='UTF-8') as module_file:
      file_text = module_file.read()

    # Check if the file contains an imports block
    imports_block = re_search(RE_IMPORT_BLOCK, file_text, flags=MULTILINE)
    if imports_block:
      imports_block = imports_block.group(0)
    else: continue

    with open(package, 'w', encoding='UTF-8') as module_file:
      # Replace the imports block with the remapped imports
      remapped_imports = imports_block
      for module, replacement in mappings:
        remapped_imports = replace_module(module, replacement, remapped_imports)

      # Write the updated file back to disk
      file_text = file_text.replace(imports_block, remapped_imports)
      module_file.seek(0)
      module_file.write(file_text)


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
