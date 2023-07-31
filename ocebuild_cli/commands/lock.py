#!/usr/bin/env python3

## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""CLI entrypoint for the lock command."""

from os import getcwd

from typing import List, Optional, Tuple, Union

import click
from rich import box
from rich.table import Table

from ocebuild.parsers.yaml import parse_yaml
from ocebuild.pipeline.lock import *
from ocebuild.sources.resolver import ResolverType

import ocebuild_cli._lib as lib
from ocebuild_cli._lib import cli_command
from ocebuild_cli.interactive import Progress, progress_bar
from ocebuild_cli.logging import *

from third_party.cpython.pathlib import Path


def rich_resolver(resolver: ResolverType,
                  resolver_props: dict,
                  resolution: str
                  ) -> Union[str, None]:
  """Returns a rich formatted specifier resolver.

  Args:
    resolver: The resolver class.
    resolver_props: The resolver properties.
    resolution: The specifier resolution.

  Returns:
    A rich formatted specifier resolver.
  """

  if resolver is None: return None
  elif 'path' in resolver_props:
    path_ = Path(resolver.path)
    # _checksum = resolver_props['__resolver'].checksum
    name, resolution_str = resolution.split('@file:')
    resolution_str = f'file:{resolution_str}' \
      .replace(':', '[/dim cyan][dim]:[/dim][dim yellow]', 1) \
      .replace(path_.name, f'[bold yellow]{path_.name}', 1) \
      .replace('#', '[/bold yellow][/dim yellow][dim]#[dim bold]') \
      .replace('=', '[/dim bold][dim]=')
  elif 'url' in resolver_props:
    has_version_ = ':' in resolution
    close_color_ = "[/green]" if has_version_ else "[/dim cyan]"
    name, resolution_str = resolution.split('@')
    resolution_str = resolution_str \
      .replace(':', '[/dim cyan][dim]:[/dim][green]', 1) \
      .replace('#', f'{ close_color_ }[dim]#[dim bold]') \
      .replace('=', '[/dim bold][dim]=')

  return f"[cyan]{name}[/cyan][dim cyan]@{resolution_str}"

def rich_revision(revision: str) -> str:
  """Returns a rich formatted revision hash.

  Args:
    revision: The revision entry.

  Returns:
    A rich formatted commit or checksum hash.
  """
  entry = parse_yaml([revision[1:-1].strip()])
  algorithm, checksum = next(iter(entry.items()))
  pad = len(str.ljust(algorithm, len('SHA256'))) - len(algorithm)
  return f"[dim bold]{algorithm}[/dim bold][dim]: {checksum[:7 + pad]}…[/dim]"

def format_resolvers(resolvers: List[dict]) -> Table:
  """Prints the resolved specifiers for the given resolvers.

  Resolvers are presented in a table with the following columns:
    - Type: The resolver type.
    - Name: The resolver name.
    - Version: The resolver version, optionally with the commit or checksum hash.
    - Resolution: The specifier resolution.

  Args:
    resolvers: A dictionary of resolver entries.

  Returns:
    A rich formatted table of the resolved specifiers.
  """

  table = Table(box=box.ROUNDED)
  table.add_column('Type', justify='right', style='bold', no_wrap=True)
  table.add_column('Name', justify='left')
  table.add_column('Version', justify='right')
  table.add_column('Resolution', justify='left')

  prev_type = None
  for entry in resolvers:
    # Extract the resolver type and resolution properties.
    type_entry = entry['__category'] if entry['__category'] != prev_type else None
    if type_entry: prev_type = type_entry
    resolution_entry = rich_resolver(resolver=entry['__resolver'],
                                     resolver_props=entry,
                                     resolution=entry['resolution'])
    # Show additional information if in debug mode.
    checksum_entry = \
      rich_revision(entry['revision']) if lib.DEBUG and 'revision' in entry else \
        None
    # Add resolver entry to the table.
    table.add_row(f"[bold]{type_entry}" if type_entry else '[dim]..',
                  f"[cyan]{entry['name']}",
                  (f"[green]{entry['version']}[/green]" if 'version' in entry \
                    else '[dim]-')
                  + (f" [dim]({checksum_entry})" if checksum_entry else ''),
                  resolution_entry if '__resolver' in entry else '')

  return table

def get_lockfile(cwd: Union[str, Path],
                 project_dir: Union[str, Path]
                 ) -> Tuple[dict, Path]:
  """Reads the project's lockfile.

  Args:
    cwd: The current working directory.
    project_dir: The project directory.

  Returns:
    A tuple containing:
      - The lockfile dictionary.
      - The lockfile metadata.
      - The lockfile path.
  """

  LOCK_FILE = Path(project_dir, 'build.lock')
  if LOCK_FILE.exists():
    info(msg=f"Found lockfile at '{LOCK_FILE.relative(cwd)}'.")
    try:
      lockfile, metadata = read_lockfile(lockfile_path=LOCK_FILE, metadata=True)
    except Exception as e: #pylint: disable=broad-exception-caught
      error(msg=f"Encountered an error while reading '{LOCK_FILE.name}': {e}",
            hint="Try running `ocebuild lock` first.")
  else:
    info(msg=f"Creating a new lockfile at '{LOCK_FILE.relative(cwd)}'.")
    lockfile, metadata = {}, {}

  return lockfile, metadata, LOCK_FILE

def resolve_lockfile(cwd: Union[str, Path],
                     check: bool=False,
                     update: bool=False,
                     force: bool=False,
                     build_config: Optional[dict]=None,
                     project_dir: Optional[Path]=None
                     ) -> Tuple[dict, List[dict], Path]:
  """Resolves the project's lockfile.

  Args:
    env: The CLI environment.
    cwd: The current working directory.
    check: Whether to check if the lockfile is consistent with the build file.
    update: Whether to update the lockfile.
    force: Whether to force the lockfile update.
    build_config: The build configuration. (Optional)
    project_dir: The project directory. (Optional)

  Returns:
    A tuple containing:
      - The lockfile dictionary.
      - The resolved specifiers.
  """

  # Read the build configuration
  if not (build_config or project_dir):
    from .build import get_build_file #pylint: disable=import-outside-toplevel
    build_config, *_, project_dir = get_build_file(cwd)

  # Read the lockfile
  lockfile, metadata, LOCKFILE = get_lockfile(cwd, project_dir=project_dir)

  # Resolve the specifiers in the build configuration
  if update: debug(msg='(--update) Updating lockfile entries...')
  if force:  debug(msg='(--force) Forcing lockfile update...')
  try:
    with Progress() as progress:
      bar = progress_bar('Resolving lockfile entries', wrap=progress)
      resolvers = resolve_specifiers(build_config, lockfile,
                                     base_path=project_dir,
                                     update=update,
                                     force=force,
                                     # Interactive arguments
                                     __wrapper=bar)
  except Exception as e: #pylint: disable=broad-exception-caught
    abort(msg=f'Failed to resolve build specifiers: {e}',
          hint='Check the build configuration for errors.')
  else:
    info(f'Resolved {len(resolvers)} total entries.')
    removed, resolved = [], {}
    if (update or force) or not lockfile:
      # Remove lockfile entries that are not in the build configuration
      removed = prune_lockfile(build_config, lockfile)
      # Filter out non-resolver entries
      resolved = [ e for e in resolvers if e['__resolver'] ]

  # Validate that the lockfile matches the build configuration
  if check:
    debug(msg='(--check) Validating lockfile entries...')
    try:
      validate_dependencies(lockfile, build_config)
    except AssertionError as e:
      abort(msg=e, traceback=False)
    else:
      success('Lockfile validation succeeded.')
      exit(0)
  # Handle updating the lockfile
  elif resolved or removed:
    # Display added lockfile entries
    if resolved:
      msg = f'Added {len(resolved)} new entries'
      if lib.VERBOSE:
        info(f'{msg}:', format_resolvers(resolved))
      else:
        info(f'{msg}.')
    # Display removed lockfile entries
    if removed:
      msg = f'Removed {len(removed)} entries'
      echo(f"{msg}.")
    # Write lockfile to disk
    lockfile = write_lockfile(LOCKFILE, lockfile, resolved, metadata)
    success(f"Lockfile written to '{LOCKFILE.relative(cwd)}'.")
  # No new resolvers
  elif lockfile and (update or force):
    success('Lockfile is up to date.')
  else:
    success('Lockfile is in sync.')

  return lockfile, resolvers


@cli_command(name='lock')
@click.option("-c", "--cwd",
              type=click.Path(exists=True,
                              file_okay=False,
                              readable=True,
                              writable=True,
                              path_type=Path),
              help="Use the specified directory as the working directory.")
@click.option("--check",
              is_flag=True,
              help="Check that lockfile is consistent with the build file.")
@click.option("--update",
              is_flag=True,
              help="Update outdated lockfile entries.")
@click.option("--force",
              is_flag=True,
              help="Force refresh even if the lockfile is up to date.")
def cli(env, cwd, check, update, force):
  """Updates the project's lockfile."""

  if not cwd: cwd = getcwd()
  else: debug(msg=f"(--cwd) Using '{cwd}' as the working directory.")

  # Process the lockfile
  resolve_lockfile(cwd, check, update, force)
  # lockfile, resolvers = resolve_lockfile(cwd, check, update, force)


__all__ = [
  # Functions (6)
  "rich_resolver",
  "rich_revision",
  "format_resolvers",
  "get_lockfile",
  "resolve_lockfile",
  "cli"
]
