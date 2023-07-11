#!/usr/bin/env python3

## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Entry point for the CLI."""

import click

from .build import cli as build


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
"""Shared context settings for the CLI."""

@click.group(context_settings=CONTEXT_SETTINGS)
def cli(): pass


def _main():
  """Main runner for the CLI."""
  cli.add_command(build)
  cli()

if __name__ == '__main__': _main()
