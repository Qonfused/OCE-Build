#!/usr/bin/env python3

## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""CLI entrypoint for the lock command."""

from os import getcwd

from typing import Optional, Tuple, Union

import click
from rich import box
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

from ._lib import abort, cli_command, CLIEnv, debug, echo, error, progress_bar

from ocebuild.pipeline.lock import read_lockfile, resolve_specifiers
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
    path = PathResolver(resolver.path)
    name, filepath = resolution.split('@file:')
    resolution_str = f'file:{filepath}' \
      .replace(':', '[/dim cyan][dim]:[/dim][dim yellow]', 1) \
      .replace(path.name, f'[bold yellow]{path.name}', 1) \
      .replace('#', '[/bold yellow][/dim yellow][dim]#[dim bold]') \
      .replace('=', '[/dim bold][dim]=')
  elif 'url' in resolver_props:
    name, resolution_str = resolution.split('@')
    resolution_str = resolution_str \
      .replace(':', '[/dim cyan][dim]:[/dim][green]', 1) \
      .replace('#', '[/dim cyan][dim]#[dim bold]') \
      .replace('=', '[/dim bold][dim]=')

  return f"[cyan]{name}[/cyan][dim cyan]@{resolution_str}"

def rich_commit(commit: str, algorithm='SHA1') -> str:
  """Returns a rich formatted commit or chechsum hash.
  
  Args:
    commit: The commit or checksum hash.
    algorithm: The algorithm used to generate the hash.

  Returns:
    A rich formatted commit or checksum hash.
  """
  return f"[dim bold]{algorithm}[/dim bold][dim]:{commit[:7]}…"

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
    from ._lib import DEBUG
    checksum = None if not DEBUG else \
      props['commit'] if 'commit' in props else \
        props['checksum'] if 'checksum' in props else \
          None
    # Add resolver entry to the table.
    table.add_row(f"[bold]{type_entry}" if type_entry else '[dim]..',
                  f"[cyan]{name}",
                  (f"[green]{entry['version']}[/green]" if 'version' in entry \
                    else '[dim]-')
                  + (f" [dim]({rich_commit(checksum)})" if checksum else ''),
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
      - The lockfile path.
  """

  LOCK_FILE = PathResolver(project_dir, 'build.lock')
  if LOCK_FILE.exists():
    debug(msg=f"Found lockfile at '{LOCK_FILE.relative(cwd)}'.")
    try:
      lockfile = read_lockfile(lockfile_path=LOCK_FILE)
    except Exception as e:
      error(msg=f"Encountered an error while reading '{LOCK_FILE.name}': {e}",
            hint="Try running `ocebuild lock` first.")
  else:
    debug(msg=f"Creating a new lockfile at '{LOCK_FILE.relative(cwd)}'.")
    lockfile = {}
  
  return lockfile, LOCK_FILE

def resolve_lockfile(env: CLIEnv,
                     cwd: Union[str, PathResolver],
                     update: bool=False,
                     force: bool=False,
                     build_config: Optional[dict]=None,
                     PROJECT_DIR: Optional[PathResolver]=None
                     ) -> Tuple[dict, dict, PathResolver]:
  """Resolves the project's lockfile.
  
  Args:
    env: The CLI environment.
    cwd: The current working directory.
    update: Whether to update the lockfile.
    force: Whether to force the lockfile update.
    build_config: The build configuration. (Optional)
    PROJECT_DIR: The project directory. (Optional)

  Returns:
    A tuple containing:
      - The lockfile dictionary.
      - The resolved specifiers.
      - The lockfile path.
  """

  # Read the build configuration
  if not (build_config or PROJECT_DIR):
    from .build import get_build_file
    build_config, *_, PROJECT_DIR = get_build_file(cwd)
  
  # Read the lockfile
  lockfile, LOCKFILE = get_lockfile(cwd, project_dir=PROJECT_DIR)
  
  # Resolve the specifiers in the build configuration
  if update: debug(msg='(--update) Updating lockfile entries...')
  if force:  debug(msg='(--force) Forcing lockfile update...')
  try:
    with Progress(transient=True) as progress:
      bar = progress_bar('Resolving build specifiers', wrap=progress)
      resolvers = resolve_specifiers(build_config, lockfile,
                                     base_path=PROJECT_DIR,
                                     update=update,
                                     force=force,
                                     # Interactive arguments
                                     __wrapper=bar)
      if not resolvers:
        echo(calls=[{'msg': '\nNothing to build.', 'fg': 'white' },
                    'Try running with `--update` or `--force` to regenerate a build.'],
             exit=0)
  except Exception as e:
    abort(msg=f'Failed to resolve build specifiers: {e}',
          hint='Check the build configuration for errors.')
  else:
    resolved = { k:v for k,v in resolvers.items() if v['__resolver'] }
    msg = f'Pending {len(resolved)} new entries (of {len(resolvers)})'
    if env.verbose:
      echo(f"\n{msg}:", fg='white')
      print_pending_resolvers(resolved)
    else:
      echo(f"\n{msg}.", fg='white')
  
  return lockfile, resolvers, LOCKFILE


@cli_command(name='lock')
@click.option("-c", "--cwd",
              type=click.Path(file_okay=False),
              help="Use the specified directory as the working directory.")
@click.option("--update",
              is_flag=True,
              help="Update outdated lockfile entries before building.")
@click.option("--force",
              is_flag=True,
              help="Force the build even if the lockfile is up to date.")
def cli(env, cwd, update, force):
  """Updates the project's lockfile."""

  if not cwd: cwd = getcwd()
  else: debug(msg=f"(--cwd) Using '{cwd}' as the working directory.")

  # Process the lockfile
  lockfile, resolvers, LOCKFILE = resolve_lockfile(env, cwd, update, force)


__all__ = [
  # Functions (6)
  "rich_resolver",
  "rich_commit",
  "print_pending_resolvers",
  "get_lockfile",
  "resolve_lockfile",
  "cli"
]
