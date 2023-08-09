#!/usr/bin/env python3

## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""CLI entrypoint for the build command."""

from os import getcwd, makedirs

from typing import List, Tuple, Union

import click

from ocebuild.filesystem import copy, glob, remove
from ocebuild.filesystem.cache import clear_cache, UNPACK_DIR
from ocebuild.parsers.dict import merge_dict, nested_del, nested_get
from ocebuild.parsers.plist import write_plist
from ocebuild.pipeline.build import *
from ocebuild.pipeline.config import update_entries
from ocebuild.pipeline.packages import *
from ocebuild.pipeline.packages import _iterate_extract_packages

from ocebuild_cli._lib import cli_command
from ocebuild_cli.interactive import Progress, progress_bar
from ocebuild_cli.logging import *

from third_party.cpython.pathlib import Path


def get_build_file(cwd: Union[str, Path]
                   ) -> Tuple[dict, dict, List[str], Path, Path]:
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
    PROJECT_DIR = Path(BUILD_FILE.parent).resolve()
    try:
      relative_path = PROJECT_DIR.relative('.')
      debug(f"Using '{relative_path}' as the project root.")
    except ValueError:
      absolute_path = cwd.joinpath(PROJECT_DIR)
      debug(f"Using {absolute_path} as the project root.")

  return build_config, build_vars, flags, BUILD_FILE, PROJECT_DIR

def unpack_packages(resolvers: List[dict], project_dir: Path) -> dict:
  """Unpacks packages to a temporary directory."""
  debug(f"Unpacking packages to {UNPACK_DIR}")
  with Progress() as progress:
    bar = progress_bar('Unpacking packages', wrap=progress)
    unpacked_entries = unpack_build_entries(resolvers,
                                            project_dir=project_dir,
                                            # Interactive arguments
                                            __wrapper=bar)
  num_unpacked = len([k for e in unpacked_entries.values() for k in e.keys()])
  if num_unpacked:
    success(f'Unpacked {num_unpacked} packages from lockfile.')

  return unpacked_entries

def extract_packages(build_vars: dict,
                     lockfile: dict,
                     resolvers: List[dict],
                     packages: dict,
                     build_dir: Path,
                     ) -> Tuple[Union[Path, None], dict]:
  """Extracts packages for build entries satisfying the build configuration."""
  extracted_entries = {}

  def count(d: dict) -> int:
    return len([k for e in d.values() for k in e.keys()])

  # Include build entries from the OpenCore package as (vendored) packages
  if opencore_pkg := nested_get(packages, ['OpenCorePkg', 'OpenCore']):
    with Progress() as progress:
      bar = progress_bar('Extracting OpenCore package', wrap=progress)
      extracted = extract_opencore_packages(opencore_pkg,
                                            target=build_vars['variables']['target'],
                                            resolvers=resolvers,
                                            packages=packages)
      extracted_entries = merge_dict(extracted_entries, extracted)
    # Show the extracted OpenCore package version
    entry = nested_get(lockfile, ['dependencies', 'OpenCorePkg', 'OpenCore'])
    success(f"Extracted OpenCore package [cyan]v{entry['version']}[/cyan].",
            highlight=False)
    # Report the number of entries bundled with the OpenCore package
    info(f"Extracted {count(extracted)} build entries from OpenCore package.")
    for category, entries in sorted(extracted.items()):
      debug(f"Extracted {len(entries)} {category} entries:")
      for entry in entries.values():
        debug(f"--> '{entry['__dest'].relative(build_dir)}'")

  # Extract remaining packages
  if packages:
    with Progress() as progress:
      bar = progress_bar('Extracting packages', wrap=progress)
      extracted = extract_build_packages(build_vars, resolvers, packages,
                                         build_dir=build_dir,
                                         # Interactive arguments
                                         __wrapper=bar)
      extracted_entries = merge_dict(extracted_entries, extracted)
    info(f"Extracted {count(extracted)} build entries from lockfile.")

  return opencore_pkg, extracted_entries

def extract_build_directory(opencore_pkg: Union[str, Path],
                            extracted_entries: dict,
                            build_dir: Path
                            ) -> None:
  """Extracts all package-extracted build entries to the build directory."""

  with Progress() as progress:
    # Extract OpenCore package to build directory (without vendored packages)
    if opencore_pkg:
      remaining_categories = set(extracted_entries.keys())
      bar1 = progress.add_task("Moving OpenCore package",
                               total=len(remaining_categories))
      def ignore_extracted(path, _):
        exclusions = set()
        if (category := Path(path).name) in remaining_categories:
          entry = nested_get(extracted_entries, [category])
          exclusions |= set(e['__extracted'].name for e in entry.values())
          remaining_categories.remove(category)
          progress.update(bar1, advance=1)
        return exclusions
      copy(opencore_pkg, build_dir, ignore=ignore_extracted, dirs_exist_ok=True)

    # Move build entries to the build directory
    bar2 = progress_bar('Moving build entries', wrap=progress)
    iterator = bar2(_iterate_extract_packages(extracted_entries))
    for category, name, entry in iterator:
      dest = entry['__dest']
      src = entry['__extracted']
      # Move and overrite existing files
      if dest.exists(): remove(dest)
      copy(src, dest)
      # Remove the entry if it failed to copy
      if not dest.exists():
        nested_del(extracted_entries, [category, name])

  # Clean up the temporary directory
  clear_cache(cache_dirs=[UNPACK_DIR])

  return extracted_entries

def update_config_entries(build_dir: Union[str, Path],
                          build_config: dict,
                          clean: bool=False
                          ) -> Path:
  """Updates the build entries in the config.plist."""
  try:
    with Progress() as progress:
      progress_bar('Updating build entries in config.plist', wrap=progress)
      # Copy sample config.plist if it does not exist
      BUILD_DIR = Path(build_dir).resolve()
      if not (config_plist := BUILD_DIR.joinpath('EFI/OC/config.plist')).exists():
        copy(BUILD_DIR.joinpath('Docs/Sample.plist'), config_plist)
        clean = True
      # Update config.plist
      updated_config = update_entries(config_plist, build_config, clean=clean)
      config_plist.write_text(write_plist(updated_config))
  except Exception as e:
    error(f"Failed to update config.plist: {e}", traceback=True)
  else:
    success(f"Updated config.plist build entries.")

  return config_plist


@cli_command(name='build')
@click.option("-c", "--cwd",
              type=click.Path(exists=True,
                              file_okay=False,
                              readable=True,
                              writable=True,
                              path_type=Path),
              help="Use the specified directory as the working directory.")
@click.option("-o", "--out",
              type=click.Path(path_type=Path),
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
  BUILD_DIR = Path(cwd, out)
  debug(f"Using '{BUILD_DIR}' as the build directory.")
  if clean:
    debug('(--clean) Cleaning the output directory...')
    try:
      remove(BUILD_DIR)
    except Exception: #pylint: disable=broad-exception-caught
      abort(f"Failed to clean the output directory ('{BUILD_DIR}')",
            'Check the output directory permissions.')
    else:
      makedirs(BUILD_DIR, exist_ok=True)
      if not any(BUILD_DIR.iterdir()):
        success(f"Cleaned the output directory at '{BUILD_DIR}'.")

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
  # Handle skipping builds if the lockfile and build dir is up to date
  has_pending_build = any(e['specifier'] != '*' and not e['__filepath'].exists()
                          for e in resolvers)
  if not (has_pending_build or BUILD_DIR.exists()):
    echo('\n[white]Nothing to build.[/white]',
         '\nTry running with --update or --force to regenerate a build.',
         log=False)
    exit(0)

  # Extract all build entries to a temporary directory
  packages = unpack_packages(resolvers, project_dir=PROJECT_DIR)
  opencore_pkg, extracted = extract_packages(build_vars, lockfile, resolvers,
                                             packages=packages,
                                             build_dir=BUILD_DIR)
  # Move build entries to the build directory
  extract_build_directory(opencore_pkg, extracted, build_dir=BUILD_DIR)
  OC_DIR = glob(BUILD_DIR, '**/OC/OpenCore.efi', first=True).parent
  if extracted:
    num_extracted = len([k for e in extracted.values() for k in e.keys()])
    extracted_dir = OC_DIR.relative(cwd)
    success(f"Extracted {num_extracted} build entries to '{extracted_dir}'.")

  # Validate build entries
  missing_entries = validate_build_directory(build_config, out_dir=BUILD_DIR)
  if missing_entries:
    num_missing = len([k for e in missing_entries.values() for k in e.keys()])
    abort(f"Could not extract {num_missing} build entries.", traceback=False)

  # Update build entries in config.plist
  config_plist = update_config_entries(BUILD_DIR, build_config, clean=clean)

  # Apply patches to config.plist
  from .patch import apply_patches #pylint: disable=import-outside-toplevel
  config = apply_patches(out=BUILD_DIR,
                         config_plist=config_plist,
                         project_root=PROJECT_DIR,
                         flags=flags)


__all__ = [
  # Functions (6)
  "get_build_file",
  "unpack_packages",
  "extract_packages",
  "extract_build_directory",
  "update_config_entries",
  "cli"
]
