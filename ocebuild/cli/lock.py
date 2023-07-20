#!/usr/bin/env python3

## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""CLI entrypoint for the lock command."""

#pylint: disable=wildcard-import,unused-wildcard-import

from os import getcwd

from typing import Optional, Tuple, Union

import click
from rich import box
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

from ._lib import abort, cli_command, CLIEnv, debug, echo, error, progress_bar

from ocebuild.parsers.yaml import parse_yaml
from ocebuild.pipeline.lock import *
from ocebuild.sources.resolver import PathResolver, ResolverType


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
    path_ = PathResolver(resolver.path)
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

def print_pending_resolvers(resolvers: dict) -> None:
  """Prints the resolved specifiers for the given resolvers.

  Resolvers are presented in a table with the following columns:
    - Type: The resolver type.
    - Name: The resolver name.
    - Version: The resolver version, optionally with the commit or checksum hash.
    - Resolution: The specifier resolution.

  Args:
    resolvers: A dictionary of resolver entries.
  """

  table = Table(box=box.ROUNDED)
  table.add_column('Type', justify='right', style='bold', no_wrap=True)
  table.add_column('Name', justify='left')
  table.add_column('Version', justify='right')
  table.add_column('Resolution', justify='left')

  prev_type = None
  for name, entry in resolvers.items():
    # Extract the resolver type and resolution properties.
    type_entry = entry['__category'] if entry['__category'] != prev_type else None
    if type_entry: prev_type = type_entry
    props = dict(entry['__resolver']) if '__resolver' in entry else {}
    resolution_entry = rich_resolver(resolver=entry['__resolver'],
                                     resolver_props=entry,
                                     resolution=entry['resolution'])
    # Show additional information if in debug mode.
    from ._lib import DEBUG #pylint: disable=import-outside-toplevel
    checksum_entry = None if not DEBUG else \
      rich_revision(entry['revision']) if 'revision' in entry else \
        None
    # Add resolver entry to the table.
    table.add_row(f"[bold]{type_entry}" if type_entry else '[dim]..',
                  f"[cyan]{name}",
                  (f"[green]{entry['version']}[/green]" if 'version' in entry \
                    else '[dim]-')
                  + (f" [dim]({checksum_entry})" if checksum_entry else ''),
                  resolution_entry if '__resolver' in entry else '')

  Console().print(table)

def get_lockfile(cwd: Union[str, PathResolver],
                 project_dir: Union[str, PathResolver]
                 ) -> Tuple[dict, PathResolver]:
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

  LOCK_FILE = PathResolver(project_dir, 'build.lock')
  if LOCK_FILE.exists():
    debug(msg=f"Found lockfile at '{LOCK_FILE.relative(cwd)}'.")
    try:
      lockfile, metadata = read_lockfile(lockfile_path=LOCK_FILE)
    except Exception as e: #pylint: disable=broad-exception-caught
      error(msg=f"Encountered an error while reading '{LOCK_FILE.name}': {e}",
            hint="Try running `ocebuild lock` first.")
  else:
    debug(msg=f"Creating a new lockfile at '{LOCK_FILE.relative(cwd)}'.")
    lockfile, metadata = {}, {}

  return lockfile, metadata, LOCK_FILE

def resolve_lockfile(env: CLIEnv,
                     cwd: Union[str, PathResolver],
                     check: bool=False,
                     update: bool=False,
                     force: bool=False,
                     build_config: Optional[dict]=None,
                     project_dir: Optional[PathResolver]=None
                     ) -> Tuple[dict, dict, PathResolver]:
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
    with Progress(transient=True) as progress:
      bar = progress_bar('Resolving lockfile entries', wrap=progress)
      resolvers = resolve_specifiers(build_config, lockfile,
                                     base_path=project_dir,
                                     update=update,
                                     force=force,
                                     # Interactive arguments
                                     __wrapper=bar)
      if not resolvers:
        echo(calls=[{'msg': '\nNothing to build.', 'fg': 'white' },
                    'Try running with `--update` or `--force` to regenerate a build.'],
             exit=0)
  except Exception as e: #pylint: disable=broad-exception-caught
    abort(msg=f'Failed to resolve build specifiers: {e}',
          hint='Check the build configuration for errors.')
  else:
    removed, resolved = [], {}
    if (update or force) or not lockfile:
      # Remove lockfile entries that are not in the build configuration
      removed = prune_lockfile(build_config, lockfile)
      # Filter out non-resolver entries
      resolved = { k:v for k,v in resolvers.items() if v['__resolver'] }

  # Validate that the lockfile matches the build configuration
  if check:
    debug(msg='(--check) Validating lockfile entries...')
    try:
      validate_dependencies(lockfile, build_config)
    except AssertionError as e:
      abort(msg=e, traceback=False)
    else:
      echo('Lockfile validation succeeded.', fg='green', exit=0)
  # Handle updating the lockfile
  elif resolved or removed:
    # Display added lockfile entries
    if resolved:
      msg = f'Added {len(resolved)} new entries'
      if env.verbose:
        echo(f"{msg}:", fg='white')
        print_pending_resolvers(resolved)
      else:
        echo(f"{msg}.", fg='white')
    # Display removed lockfile entries
    if removed:
      msg = f'Removed {len(removed)} entries'
      echo(f"{msg}.", fg='white')
    # Write lockfile to disk
    echo('Writing lockfile to disk...')
    write_lockfile(LOCKFILE, lockfile, resolved, metadata)
    echo('Done.', fg='white')
  # No new resolvers
  elif lockfile and (update or force):
    echo('Lockfile is up to date.', fg='white')
  else:
    echo('Lockfile is in sync.', fg='white')

  return lockfile, resolvers


@cli_command(name='lock')
@click.option("-c", "--cwd",
              type=click.Path(exists=True,
                              file_okay=False,
                              readable=True,
                              writable=True,
                              path_type=PathResolver),
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
  resolve_lockfile(env, cwd, check, update, force)
  # lockfile, resolvers = resolve_lockfile(env, cwd, check, update, force)


__all__ = [
  # Functions (6)
  "rich_resolver",
  "rich_revision",
  "print_pending_resolvers",
  "get_lockfile",
  "resolve_lockfile",
  "cli"
]
