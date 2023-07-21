#!/usr/bin/env python3

## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""CLI entrypoint for the patch command."""

import click
from rich.progress import Progress

from ._lib import *

from ocebuild.pipeline.config import merge_configs, read_config
from ocebuild.sources.resolver import PathResolver


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
