#!/usr/bin/env python3

## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""CLI entrypoint for the patch command."""

import click

from ocebuild.pipeline.config import merge_configs, read_config
from ocebuild.sources.resolver import PathResolver

from ocebuild_cli._lib import cli_command
from ocebuild_cli.interactive import Progress, progress_bar
from ocebuild_cli.logging import *


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


__all__ = [
  # Functions (1)
  "cli"
]
