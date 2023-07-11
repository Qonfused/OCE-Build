#!/usr/bin/env python3

## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""CLI entrypoint for the build command."""

from os import getcwd

import click
from rich.progress import Progress

from ._lib import echo, error, progress_bar

from ocebuild.errors import PathValidationError
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

  BUILD_DIR = PathResolver(cwd, out)
  if clean:
    try:
      remove(BUILD_DIR)
    except Exception as e:
      error(msg=f'Failed to clean the output directory ({BUILD_DIR})',
            hint='Check the output directory permissions.',
            label='Abort', traceback=True, suppress=[__file__])

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
  if LOCK_FILE.exists():
    try:
      lockfile = read_lockfile(lockfile_path=LOCK_FILE)
      if not lockfile:
        raise AssertionError('The lockfile is empty.')
    except Exception as e:
      error(msg=f"Encountered an error while reading '{LOCK_FILE.name}': {e}",
            hint="Try running `ocebuild lock` first.")
  else:
    lockfile = {}
  
  # Resolve the specifiers in the build configuration
  try:
    with Progress(transient=True) as progress:
      bar = progress_bar('Resolving build specifiers', wrap=progress)
      resolvers = resolve_specifiers(build_config, lockfile,
                                    base_path=PROJECT_DIR,
                                    update=update,
                                    force=force,
                                    # Interactive arguments
                                    __wrapper=bar)
  except Exception as e:
    error(msg=f'Failed to resolve build specifiers: {e}',
          hint='Check the build configuration for errors.',
          label='Abort', traceback=True, suppress=[__file__])
  else:
    if not resolvers:
      echo(calls=[{'msg': '\nNothing to build.', 'fg': 'white' },
                  'Try running with `--update` or `--force` to regenerate a build.'],
           exit=0)
  
  # Extract the OpenCore package to the output directory
  try:
    with Progress(transient=True) as progress:
      bar = progress_bar('Extracting OpenCore package', wrap=progress)
      OC_DIR = extract_opencore_directory(resolvers,
                                          lockfile,
                                          target=build_vars['variables']['target'],
                                          out_dir=BUILD_DIR,
                                          # Interactive arguments
                                          __wrapper=bar)
    # Validate that the OpenCore directory was extracted
    if not OC_DIR:
      raise RuntimeError('The OpenCore package was not extracted.')
    if not (OC_DIR.exists() and set(OC_DIR.iterdir())):
      raise PathValidationError('The extracted OpenCore package is empty.',
                                name=OC_DIR.name,
                                path=OC_DIR,
                                kind='Directory')
    # Validate that the OpenCore binary was extracted
    oc_config = nested_get(build_config, ['OpenCorePkg', 'OpenCore'])
    oc_binary = PathResolver(BUILD_DIR, oc_config['__filepath'])
    if not (oc_binary.exists() and OC_DIR.joinpath(oc_binary.name).exists()):
      raise PathValidationError('The extracted OpenCore package is malformed.',
                                name=oc_binary.name,
                                path=oc_binary,
                                kind='Binary')
  except PathValidationError as e:
    error(msg=f'Failed to extract the OpenCore package: {e}',
          hint='Check the OpenCore build configuration for errors.')
  except Exception as e:
    error(msg=f'Encountered an error while extracting the OpenCore package',
          label='Abort', traceback=True, suppress=[__file__])
