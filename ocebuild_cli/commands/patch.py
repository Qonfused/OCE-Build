#!/usr/bin/env python3

## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""CLI entrypoint for the patch command."""

from os import getcwd

from typing import List, Optional, Tuple, Union

import click

from ocebuild.filesystem import glob
from ocebuild.parsers.dict import nested_get
from ocebuild.parsers.plist import write_plist
from ocebuild.parsers.regex import re_search
from ocebuild.pipeline.config import *
from ocebuild.pipeline.lock import read_lockfile

from ocebuild_cli._lib import cli_command
from ocebuild_cli.interactive import Progress, progress_bar
from ocebuild_cli.logging import *

from third_party.cpython.pathlib import Path


def get_schema(cwd: Union[str, Path]='.',
                lockfile: Optional[dict]=None,
                **kwargs
                ) -> Union[dict, Tuple[dict, dict]]:
  """Reads the Sample.plist schema from the resolved OpenCorePkg version.

  If a lockfile is provided or located in the current working directory, the
  resolved OpenCorePkg version will be used to fetch the Sample.plist schema.

  In case no lockfile is provided or no OpenCorePkg dependency is found, the
  latest version of the Sample.plist schema will be used.

  Args:
    cwd: The current working directory (Optional).
    lockfile: The lockfile to read the OpenCore version from (Optional).
    kwargs: Additional keyword arguments to pass to `get_configuration_schema`.

  Returns:
    A dictionary representing failsafe values for the Sample.plist schema.
  """

  if not lockfile:
    # Attempt to read the lockfile
    LOCKFILE = glob(cwd, '**/build.lock', first=True)
    lockfile = read_lockfile(LOCKFILE) if LOCKFILE.exists() else {}

  # Attempt to read the resolved OpenCorePkg commit
  entry = nested_get(lockfile, ('dependencies', 'OpenCorePkg', 'OpenCore'), {})
  commit_sha = re_search('(?<=#commit=)[a-f0-9]+', entry.get('resolution'))
  if commit_sha:
    info(f"Using Sample.plist schema for commit [cyan]{commit_sha[:7]}[/cyan]")

  return get_configuration_schema(commit=commit_sha, **kwargs)

def apply_patches(cwd: Union[str, Path]='.',
                  out: Union[str, Path]='.',
                  *patches: List[Union[str, Path]],
                  config_plist: Optional[Union[str, Path]]=None,
                  project_root: Optional[Union[str, Path]]=None,
                  flags: Optional[List[str]]=None,
                  sort_keys: bool=True
                  ) -> dict:
  """Applies configuration patches to the config.plist.

  This function will attempt to locate the config.plist and project root
  relative to the current working directory. If the config.plist is not given,
  the function will attempt to locate the config.plist relative to the output
  directory.

  Patches (`config*.{yml|yaml}` or `patch*.{yml|yaml}` files) located under the
  project root are applied to the config.plist in the order they are found.

  If any of the entries of the configuration file or patches are missing any
  required keys dictated by the Sample.plist schema, the failsafe values will
  be used to insert the missing keys.

  Args:
    cwd: The current working directory (Default: the current working directory).
    out: The output directory (Default: the current working directory).
    patches: A list of paths to configuration patches (Optional).
    config_plist: The path to the config.plist (Optional).
    project_root: The path to the project root (Optional).
    flags: A list of flags to pass to `merge_configs` (Optional).
    sort_keys: Whether to sort the keys of the config.plist (Default: True).

  Returns:
    A dictionary representing the patched config.plist.
  """

  if not config_plist:
    config_plist = glob(out, '**/OC/config.plist', first=True)

  if not project_root:
    # Locate the project root relative to the build configuration
    build_file = glob(cwd, '**/build.yml', include='**/build.yaml', first=True)
    if build_file:
      project_root = build_file.parent
    # Fall back to the current working directory
    else: project_root = cwd

  # Extract the Sample.plist schema
  schema, sample = get_schema(cwd=project_root, get_sample=True)

  # Extract configuration patches
  if not patches:
    patches = set(glob(project_root, '**/config*.yml', include='**/config*.yaml'))
    patches |= set(glob(project_root, '**/patch*.yml', include='**/patch*.yaml'))
    debug(f"Found {len(patches)} patch files")
  elif cwd:
    patches = set(Path(cwd, patch).resolve(strict=True) for patch in patches)

  # Apply patches and schema fallbacks to the config.plist
  try:
    with Progress() as progress:
      progress_bar(progress, "Applying patches to config.plist")
      # Apply patches and schema defaults
      merged = merge_configs(config_plist, *patches, flags=flags)
      config = apply_schema_defaults(merged, schema, sample)
      # Write the patched config.plist
      config_plist.write_text(write_plist(config, sort_keys=sort_keys))
  except Exception as e:
    error(f"Failed to update config.plist: {e}", traceback=True)
  else:
    name = 'file' if len(patches) == 1 else 'files'
    success(f"Updated config.plist with {len(patches)} patch {name}.")

  return config


@cli_command(name='patch')
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
@click.option("-p", "--patches",
              type=click.Path(path_type=Path),
              multiple=True,
              help="A list of paths to configuration patches.")
def cli(env, cwd, out, patches):
  """Patches an existing OpenCore configuration."""

  if not cwd: cwd = getcwd()
  else: debug(f"(--cwd) Using '{cwd}' as the working directory.")

  if not out: out = 'dist'
  else: debug(f"(--out) Using '{out}' as the build directory.")

  #TODO: Re-use cwd and out parameter wrappers to resolve the build directory
  BUILD_DIR = Path(cwd, out)

  #TODO: Add additional options to the CLI
  # config = apply_patches(cwd, out)
  apply_patches(cwd, BUILD_DIR, *patches)


__all__ = [
  # Functions (3)
  "get_schema",
  "apply_patches",
  "cli"
]
