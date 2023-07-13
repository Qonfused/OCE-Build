#!/usr/bin/env python3

## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""CLI entrypoint for the build command."""

from os import getcwd

from typing import List, Tuple, Union

import click
from rich.progress import Progress

from ._lib import abort, cli_command, CLIEnv, debug, error, progress_bar

from ocebuild.errors import PathValidationError
from ocebuild.filesystem import glob, remove
from ocebuild.parsers.dict import nested_get
from ocebuild.pipeline.build import read_build_file
from ocebuild.pipeline.opencore import extract_opencore_directory
from ocebuild.sources.resolver import PathResolver


def get_build_file(cwd: Union[str, PathResolver]
                   ) -> Tuple[dict, dict, List[str], PathResolver, PathResolver]:
  """Read the build configuration"""
  BUILD_FILE = glob(cwd, '**/build.yml', include='**/build.yaml', first=True)
  try:
    if BUILD_FILE:
      debug(msg=f"Found build configuration at '{BUILD_FILE.relative(cwd)}'.")
      build_config, build_vars, flags = read_build_file(filepath=BUILD_FILE)
    else:
      error(msg="Could not find 'build.{yml,yaml}'",
            hint="Try running `ocebuild init` first.")
  except Exception as e:
    abort(msg=f"Encountered an error while reading '{BUILD_FILE.name}': {e}",
          hint='Check the build configuration for errors.',)
  else: 
    PROJECT_DIR = PathResolver(BUILD_FILE.parent)
    debug(msg=f"Using '{PROJECT_DIR.relative('.')}' as the project root.")
  
  return build_config, build_vars, flags, BUILD_FILE, PROJECT_DIR

def extract_opencore_pkg(cwd: Union[str, PathResolver],
                         build_config: dict,
                         build_vars: dict,
                         resolvers: dict,
                         lockfile: dict,
                         out_dir: Union[str, PathResolver]
                         ) -> PathResolver:
  """Extracts the OpenCore package to the output directory"""
  try:
    with Progress(transient=True) as progress:
      bar = progress_bar('Extracting OpenCore package', wrap=progress)
      OC_DIR = extract_opencore_directory(resolvers,
                                          lockfile,
                                          target=build_vars['variables']['target'],
                                          out_dir=out_dir,
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
    oc_binary = PathResolver(out_dir, oc_config['__filepath'])
    if not (oc_binary.exists() and OC_DIR.joinpath(oc_binary.name).exists()):
      raise PathValidationError('The extracted OpenCore package is malformed.',
                                name=oc_binary.name,
                                path=oc_binary,
                                kind='Binary')
  except PathValidationError as e:
    error(msg=f'Failed to extract the OpenCore package: {e}',
          hint='Check the OpenCore build configuration for errors.')
  except Exception as e:
    abort(msg=f'Encountered an error while extracting the OpenCore package')
  else:
    OC_DIR = PathResolver(cwd, OC_DIR.resolve())
    debug(msg=f"Extracted OpenCore binaries to '{OC_DIR.relative(cwd)}'.")

  return OC_DIR


@cli_command(name='build')
@click.option("-c", "--cwd",
              type=click.Path(file_okay=False),
              help="Use the specified directory as the working directory.")
@click.option("-o", "--out",
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
def cli(env, cwd, out, clean, update, force):
  """Builds the project's OpenCore EFI directory."""

  if not cwd: cwd = getcwd()
  else: debug(msg=f"(--cwd) Using '{cwd}' as the working directory.")
  
  if not out: out = 'dist'
  else: debug(msg=f"(--out) Using '{out}' as the build directory.")

  # Prepare the build directory
  BUILD_DIR = PathResolver(cwd, out)
  if clean:
    debug(msg='(--clean) Cleaning the output directory...')
    try:
      remove(BUILD_DIR)
    except Exception:
      abort(msg=f'Failed to clean the output directory ({BUILD_DIR})',
            hint='Check the output directory permissions.')

  # Read the build configuration
  build_config, build_vars, flags, *_, PROJECT_DIR = get_build_file(cwd)

  # Read the lockfile
  from .lock import resolve_lockfile
  lockfile, resolvers, LOCKFILE = resolve_lockfile(env, cwd, update, force,
                                                   build_config=build_config,
                                                   PROJECT_DIR=PROJECT_DIR)

  # Extract the OpenCore package to the output directory
  OC_DIR = extract_opencore_pkg(cwd,
                                build_config, build_vars,
                                resolvers, lockfile,
                                out_dir=BUILD_DIR)
