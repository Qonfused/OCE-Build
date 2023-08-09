#!/usr/bin/env python3

## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Entry point for the CLI."""

from os import _exit as os_exit

from typing import Optional

import click

from ocebuild.filesystem.cache import clear_cache, UNPACK_DIR
from ocebuild.version import __version__

from ocebuild_cli._lib import CLIEnv, CONTEXT_SETTINGS
from ocebuild_cli.commands import cli_commands
from ocebuild_cli.logging import _format_url, abort


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(message='ocebuild-cli %(version)s', version=__version__)
@click.pass_context
def cli(ctx):
  """Main runner for the CLI."""
  ctx.obj = CLIEnv()

def cli_exit(env: Optional[CLIEnv]=None, status: int=0):
  """Cleanup the CLI environment on exit."""

  # Attempt to get the CLI environment from the current context.
  if not env and (ctx := click.get_current_context(silent=True)):
    env = ctx.find_object(CLIEnv) if ctx else None

  clear_cache([UNPACK_DIR])
  os_exit(status)

@cli.result_callback(replace=True)
@click.make_pass_decorator(CLIEnv)
def cli_exit_hook(env, res, status: int=0):
  """Exit hook for CLI commands."""
  cli_exit(env, status)


def _main():
  """Entry point for the CLI."""
  try:
    for command in cli_commands:
      cli.add_command(command)
    cli() #pylint: disable=no-value-for-parameter
  # Cleanup the CLI environment on exit.
  except SystemExit as e:
    cli_exit(status=e.code or 0)
  # Catch any unhandled exceptions.
  except Exception: #pylint: disable=broad-exception-caught
    issues_url = _format_url("https://github.com/Qonfused/OCE-Build/issues")
    abort(msg="An unexpected error occurred.",
          hint=f"Please report this issue at {issues_url}.")

if __name__ == '__main__': _main()
