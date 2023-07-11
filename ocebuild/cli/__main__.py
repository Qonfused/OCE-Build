#!/usr/bin/env python3

## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Entry point for the CLI."""

import click

from ._lib import _format_url, error
from .build import cli as build


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
"""Shared context settings for the CLI."""

@click.group(context_settings=CONTEXT_SETTINGS)
def cli(): pass


def _main():
  """Main runner for the CLI."""
  cli.add_command(build)
  cli()

if __name__ == '__main__':
  try: _main()
  except Exception:
    _rich_traceback_omit = True
    issues_url = _format_url("https://github.com/Qonfused/OCE-Build/issues")
    error(msg="An unexpected error occurred.",
          label='Abort',
          hint=f"Please report this issue at {issues_url}.",
          traceback=True)

