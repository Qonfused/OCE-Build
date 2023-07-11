#!/usr/bin/env python3

## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""CLI entrypoint for the build command."""

from os import getcwd

import click

from ._lib import echo, error, progress_bar

from ocebuild.filesystem import glob, remove
from ocebuild.parsers.dict import nested_get
from ocebuild.pipeline.build import read_build_file
from ocebuild.pipeline.lock import read_lockfile, resolve_specifiers
from ocebuild.pipeline.opencore import extract_opencore_directory
from ocebuild.sources.resolver import PathResolver


@click.command(name="build")
@click.option("-c", "--cwd",
              default=getcwd(),
              type=click.Path(file_okay=False),
              help="Use the specified directory as the project root.")
@click.option("-o", "--out",
              default='dist',
              type=click.Path(file_okay=False),
              help="Use the specified directory as the output directory.")
@click.option("--clean",
              is_flag=True,
              help="Clean the output directory before building.")
@click.option("--update",
              is_flag=True,
              help="Update outdated lockfile entries before building.")
@click.option("--force",
              is_flag=True,
              help="Force the build even if the lockfile is up to date.")
def cli(cwd, out, clean, update, force):
  """Builds the project's OpenCore EFI directory."""

  if cwd:
    echo(msg=f"(--cwd) Using '{cwd}' as the project root...", dim=True)

  BUILD_DIR = PathResolver(cwd, out)
  if clean:
    echo(msg='(--clean) Cleaning output directory...', dim=True)
    remove(BUILD_DIR)

  # Read the build configuration
  BUILD_FILE = glob(cwd, '**/build.yml', include='**/build.yaml', first=True)
  try:
    build_config, build_vars, flags = read_build_file(filepath=BUILD_FILE)
  except:
    error(msg="Could not find 'build.{yml,yaml}'",
          hint="Try running `ocebuild init` first.")
  else: 
    PROJECT_DIR = PathResolver(BUILD_FILE.parent)

  # Read the lockfile
  LOCK_FILE = PathResolver(PROJECT_DIR, 'build.lock')
  try:
    if LOCK_FILE.exists():
      lockfile = read_lockfile(lockfile_path=LOCK_FILE)
      if not lockfile:
        raise AssertionError('The lockfile is empty.')
  except Exception as e:
    error(msg=f"Encountered an error while reading 'build.lock': {e}",
          hint="Try running `ocebuild lock` first.")
  
  # Resolve the specifiers in the build configuration
  if update: echo(msg='(--update) Updating lockfile entries...', dim=True)
  if force:  echo(msg='(--force) Forcing build...', dim=True)
  try:
    resolvers = resolve_specifiers(build_config, lockfile,
                                   base_path=PROJECT_DIR,
                                   update=update,
                                   force=force,
                                   # Interactive arguments
                                   __wrapper=progress_bar('Resolving build specifiers'))
  except Exception as e:
    error(msg=f'Failed to resolve build specifiers: {e}',
          hint='Check the build configuration for errors.')
  else:
    if not resolvers:
      echo(calls=[{'msg': '\nNothing to build.', 'fg': 'white' },
                  'Try running with `--update` or `--force` to regenerate a build.'],
           exit=0)
  
  # Extract the OpenCore package to the output directory
  try:
    OC_DIR = extract_opencore_directory(resolvers,
                                        lockfile,
                                        target=build_vars['variables']['target'],
                                        out_dir=BUILD_DIR,
                                        # Interactive arguments
                                        __wrapper=progress_bar('Extracting OpenCore package'))
    # Validate that the OpenCore directory was extracted
    if not OC_DIR or not (OC_DIR.exists() and set(OC_DIR.iterdir())):
      raise AssertionError('The extracted OpenCore package is empty.')
    # Validate that the OpenCore binary was extracted
    oc_config = nested_get(build_config, ['OpenCorePkg', 'OpenCore'])
    oc_binary = PathResolver(BUILD_DIR, oc_config['__filepath'])
    if not (oc_binary.exists() and OC_DIR.joinpath(oc_binary.name).exists()):
      raise AssertionError('The extracted OpenCore package is malformed.')
  except Exception as e:
    error(msg=f'Failed to extract OpenCore package: {e}',
          hint='Check the OpenCore build configuration for errors.')
