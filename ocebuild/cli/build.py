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

from ._lib import abort, cli_command, debug, echo, error, progress_bar

from ocebuild.filesystem import glob, remove
from ocebuild.parsers.dict import nested_get
from ocebuild.pipeline import config, kexts, opencore, ssdts
from ocebuild.pipeline.build import read_build_file, unpack_build_entries
from ocebuild.pipeline.lock import prune_resolver_entry
from ocebuild.sources.resolver import PathResolver


def get_build_file(cwd: Union[str, PathResolver]
                   ) -> Tuple[dict, dict, List[str], PathResolver, PathResolver]:
  """Reads the build file configuration.

  Args:
    cwd: The current working directory.

  Returns:
    A tuple containing:
      - The build configuration.
      - The build variables.
      - The build flags.
      - The build file path.
      - The project directory.
  """
  BUILD_FILE = glob(cwd, '**/build.yml', include='**/build.yaml', first=True)
  try:
    if BUILD_FILE:
      debug(msg=f"Found build configuration at '{BUILD_FILE.relative(cwd)}'.")
      build_config, build_vars, flags = read_build_file(filepath=BUILD_FILE)
    else:
      error(msg="Could not find 'build.{yml,yaml}'",
            hint="Try running `ocebuild init` first.")
  except Exception as e: #pylint: disable=broad-exception-caught
    abort(msg=f"Encountered an error while reading '{BUILD_FILE.name}': {e}",
          hint='Check the build configuration for errors.',)
  else:
    PROJECT_DIR = PathResolver(BUILD_FILE.parent)
    debug(msg=f"Using '{PROJECT_DIR.relative('.')}' as the project root.")

  return build_config, build_vars, flags, BUILD_FILE, PROJECT_DIR


@cli_command(name='build')
@click.option("-c", "--cwd",
              type=click.Path(exists=True,
                              file_okay=False,
                              readable=True,
                              writable=True,
                              path_type=PathResolver),
              help="Use the specified directory as the working directory.")
@click.option("-o", "--out",
              type=click.Path(path_type=PathResolver),
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
    except Exception: #pylint: disable=broad-exception-caught
      abort(msg=f'Failed to clean the output directory ({BUILD_DIR})',
            hint='Check the output directory permissions.')

  # Read the build configuration
  build_config, build_vars, flags, *_, PROJECT_DIR = get_build_file(cwd)

  # Read the lockfile
  from .lock import resolve_lockfile #pylint: disable=import-outside-toplevel
  lockfile, resolvers = resolve_lockfile(env, cwd,
                                         update=update,
                                         force=force,
                                         build_config=build_config,
                                         project_dir=PROJECT_DIR)
  # Prepend build directory to resolver paths
  for e in resolvers:
    e['__filepath'] = BUILD_DIR.joinpath(e['__filepath']).resolve()
  #TODO: Handle skipping builds if the lockfile and build dir is up to date
  has_pending_build = any(e['specifier'] != '*' and not e['__filepath'].exists()
                          for e in resolvers)
  if not (has_pending_build or BUILD_DIR.exists()):
    echo(calls=[{'msg': '\nNothing to build.', 'fg': 'white' },
                'Try running with --update or --force to regenerate a build.'],
         exit=0)

  # Unpack all build entries to a temporary directory
  with Progress(transient=True) as progress:
    bar = progress_bar('Extracting build packages', wrap=progress)
    unpacked_entries = unpack_build_entries(resolvers,
                                            project_dir=PROJECT_DIR,
                                            # Interactive arguments
                                            __wrapper=bar)

  # Extract the OpenCore package to the output directory
  if opencore_pkg := nested_get(unpacked_entries, ['OpenCorePkg', 'OpenCore']):
    with Progress(transient=True) as progress:
      bar = progress_bar('Extracting OpenCore package', wrap=progress)
      target = build_vars['variables']['target']
      opencore_pkg = opencore.extract_opencore_archive(pkg=opencore_pkg,
                                                       target=target)
      # Extract additional OpenCore binaries not shipped in the main package
      if binary_pkg := nested_get(unpacked_entries, ['OpenCorePkg', 'OcBinaryData']):
        opencore.extract_ocbinary_archive(pkg=binary_pkg, oc_pkg=opencore_pkg)
      # Prune remaining files from the OpenCore package
      opencore.prune_opencore_archive(opencore_pkg, resolvers,
                                      out_dir=BUILD_DIR,
                                      # Interactive arguments
                                      __wrapper=bar)
    # Cleanup resolver entries
    prune_resolver_entry(resolvers, key='__category', value='OpenCorePkg')


__all__ = [
  # Functions (2)
  "get_build_file",
  "cli"
]
