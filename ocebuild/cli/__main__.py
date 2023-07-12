#!/usr/bin/env python3

## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Entry point for the CLI."""

from os import _exit as os_exit

import click

from ._lib import _format_url, abort, CLIEnv, CONTEXT_SETTINGS
from .build import cli as build
from .lock import cli as lock


@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(ctx):
  """Main runner for the CLI."""
  ctx.obj = CLIEnv()


def _main():
  """Entry point for the CLI."""
  try:
    cli.add_command(build)
    cli.add_command(lock)
    cli()
  # Cleanup the CLI environment on exit.
  except SystemExit as e:
    os_exit(e.code or 0)
  # Catch any unhandled exceptions.
  except Exception:
    issues_url = _format_url("https://github.com/Qonfused/OCE-Build/issues")
    abort(msg="An unexpected error occurred.",
          hint=f"Please report this issue at {issues_url}.")

if __name__ == '__main__': _main()
