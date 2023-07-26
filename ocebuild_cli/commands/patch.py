#!/usr/bin/env python3

## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""CLI entrypoint for the patch command."""

import click

from typing import Optional

from ocebuild.filesystem import glob
from ocebuild.parsers.dict import nested_get
from ocebuild.parsers.plist import write_plist
from ocebuild.parsers.regex import re_search
from ocebuild.pipeline.config import *
from ocebuild.pipeline.lock import read_lockfile
from ocebuild.sources.resolver import PathResolver

from ocebuild_cli._lib import cli_command
from ocebuild_cli.interactive import Progress, progress_bar
from ocebuild_cli.logging import *


def read_schema(lockfile: Optional[dict]=None, **kwargs) -> dict:
  """Reads the Sample.plist schema from the resolved OpenCorePkg version.

  In case no lockfile is provided or no OpenCorePkg dependency is found, the
  latest version of the Sample.plist schema will be used.

  Args:
    lockfile: The lockfile to read the OpenCore version from (Optional).
    kwargs: Additional keyword arguments to pass to `get_configuration_schema`.

  Returns:
    A dictionary representing failsafe values for the Sample.plist schema.
  """

  # Attempt to read the resolved OpenCorePkg commit
  entry = nested_get(lockfile, ('dependencies', 'OpenCorePkg', 'OpenCore'), {})
  commit_sha = re_search('(?<=#commit=)[a-f0-9]+', entry.get('resolution'))
  if commit_sha:
    info(f"Using Sample.plist schema for commit {entry.get('version')[:7]}")

  return get_configuration_schema(commit=commit_sha, **kwargs)

@cli_command(name='patch')
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
def cli(env, cwd, out):
  """Patches an existing OpenCore configuration."""

  # Attempt to read the lockfile
  LOCKFILE = glob(cwd, '**/build.lock', first=True)
  lockfile = read_lockfile(LOCKFILE) if LOCKFILE.exists() else None

  # Extract the Sample.plist schema
  schema = read_schema(lockfile)

  # # Uncomment to dump the schema output to a file
  # from pprint import pprint; pprint(schema, stream=open('Schema.txt', 'w'))
  # with open('Schema.plist', 'w') as file:
  #   file.write(write_plist(schema))


__all__ = [
  # Functions (1)
  "cli"
]
