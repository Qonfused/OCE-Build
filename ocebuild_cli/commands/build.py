#!/usr/bin/env python3

## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""CLI entrypoint for the build command."""

from os import getcwd

from typing import List, Tuple, Union

import click

from ocebuild.filesystem import copy, glob, remove
from ocebuild.filesystem.cache import UNPACK_DIR
from ocebuild.parsers.dict import nested_get
from ocebuild.pipeline import config, kexts, opencore, ssdts
from ocebuild.pipeline.build import *
from ocebuild.pipeline.lock import prune_resolver_entry
from ocebuild.sources.resolver import PathResolver

from ocebuild_cli._lib import cli_command
from ocebuild_cli.interactive import Progress, progress_bar
from ocebuild_cli.logging import *


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
      info(f"Found build configuration at '{BUILD_FILE.relative(cwd)}'.")
      build_config, build_vars, flags = read_build_file(filepath=BUILD_FILE)
    else:
      error("Could not find 'build.{yml,yaml}'",
            "Try running `ocebuild init` first.")
  except Exception as e: #pylint: disable=broad-exception-caught
    abort(f"Encountered an error while reading '{BUILD_FILE.name}': {e}",
          'Check the build configuration for errors.')
  else:
    PROJECT_DIR = PathResolver(BUILD_FILE.parent)
    debug(f"Using '{PROJECT_DIR.relative('.')}' as the project root.")

  return build_config, build_vars, flags, BUILD_FILE, PROJECT_DIR

def unpack_packages(build_config: dict,
                    build_vars: dict,
                    lockfile: dict,
                    resolvers: List[dict],
                    project_dir: PathResolver,
                    build_dir: PathResolver
                    ) -> dict:
  """Unpacks and extracts packages to a temporary directory."""

  # Handle unpacking build packages from the resolvers
  debug(f"Unpacking packages to {UNPACK_DIR}")
  with Progress() as progress:
    bar = progress_bar('Unpacking packages', wrap=progress)
    unpacked_entries = unpack_build_entries(resolvers,
                                            project_dir=project_dir,
                                            # Interactive arguments
                                            __wrapper=bar)
  num_packages = len([e['name'] for e in resolvers if '__extracted' in e])
  info(f'Unpacked {num_packages} packages.')

  # Extract the OpenCore package to the output directory
  if opencore_pkg := nested_get(unpacked_entries, ['OpenCorePkg', 'OpenCore']):
    with Progress() as progress:
      bar1 = progress_bar('Extracting OpenCore package', wrap=progress)
      target = build_vars['variables']['target']
      opencore_pkg = opencore.extract_opencore_archive(pkg=opencore_pkg,
                                                       target=target)
      # Extract additional OpenCore binaries not shipped in the main package
      if binary_pkg := nested_get(unpacked_entries, ['OpenCorePkg', 'OcBinaryData']):
        opencore.extract_ocbinary_archive(pkg=binary_pkg, oc_pkg=opencore_pkg)
      # Cleanup resolver entries
      prune_resolver_entry(resolvers, key='__category', value='OpenCorePkg')
      # Prune remaining files from the OpenCore package
      opencore.prune_opencore_archive(opencore_pkg, resolvers,
                                      # Interactive arguments
                                      __wrapper=bar1)
      #TODO Copy the extracted package to the build directory
    num_oc_packages = len(unpacked_entries['OpenCorePkg'])
    info(f"Extracted {num_oc_packages} OpenCore packages.")

  # Extract remaining packages to the output directory
  if unpacked_entries:
    with Progress() as progress:
      # Extract and parse metadata from each unpacked package
      bar1 = progress_bar('Extracting packages', wrap=progress)
      extracted = extract_build_packages(build_vars, lockfile, unpacked_entries,
                                         build_dir=build_dir,
                                         # Interactive arguments
                                         __wrapper=bar1)
      # Prune extracted entries based on the build configuration
      prune_build_packages(build_config, extracted,
                           # Interactive arguments
                           __wrapper=bar1)
    num_extracted = len([k for e in extracted.values() for k in e.keys()])
    info(f"Extracted {num_extracted} build packages.")

  # Check if any packages failed to extract
  if missing_packages := num_packages - (num_oc_packages + num_extracted):
    abort(f"Failed to extract {missing_packages} packages.",
          hint="Check the build configuration for errors.",
          traceback=False)

  return extracted


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
  else: debug(f"(--cwd) Using '{cwd}' as the working directory.")

  if not out: out = 'dist'
  else: debug(f"(--out) Using '{out}' as the build directory.")

  # Prepare the build directory
  BUILD_DIR = PathResolver(cwd, out)
  debug(f"Using '{BUILD_DIR}' as the build directory.")
  if clean:
    debug('(--clean) Cleaning the output directory...')
    try:
      remove(BUILD_DIR)
    except Exception: #pylint: disable=broad-exception-caught
      abort(f"Failed to clean the output directory ('{BUILD_DIR}')",
            'Check the output directory permissions.')

  # Read the build configuration
  build_config, build_vars, flags, *_, PROJECT_DIR = get_build_file(cwd)

  # Read the lockfile
  from .lock import resolve_lockfile #pylint: disable=import-outside-toplevel
  lockfile, resolvers = resolve_lockfile(cwd,
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
    echo("\n".join(('\n[white]Nothing to build.[/white]',
                  'Try running with --update or --force to regenerate a build.')),
         log=True)
    exit(0)

  # Unpack all build entries to a temporary directory
  extracted = unpack_packages(build_config, build_vars, lockfile, resolvers,
                              project_dir=PROJECT_DIR,
                              build_dir=BUILD_DIR)


__all__ = [
  # Functions (3)
  "get_build_file",
  "unpack_packages",
  "cli"
]
