#!/usr/bin/env python3

## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Entry point for the CLI."""

from os import _exit as os_exit
from urllib.parse import urlparse

from typing import Optional

import click

from ocebuild.filesystem.cache import clear_cache, UNPACK_DIR
from ocebuild.version import __version__

from ocebuild_cli._lib import CLIEnv, CONTEXT_SETTINGS
from ocebuild_cli.commands import cli_commands
from ocebuild_cli.logging import _format_url, abort


class PassthroughCommand(click.Group):
  """A custom command group that handles the exec option specially."""

  @staticmethod
  def is_url(s):
    try:
      result = urlparse(s)
      return all([result.scheme, result.netloc])
    except ValueError:
      return False

  def parse_args(self, ctx, args):
    ctx.obj = CLIEnv()

    # Check if -e or --exec is in args
    if '-e' in args or '--exec' in args:
      # Find the position of -e or --exec
      try:
        idx = args.index('-e')
      except ValueError:
        idx = args.index('--exec')

      # Get the script path (next argument after -e/--exec)
      if idx + 1 < len(args):
        script_path = args[idx + 1]

        # If the script is a URL, we should download it to a tmp dir
        if self.is_url(script_path):
          from ocebuild.sources import request
          from tempfile import TemporaryDirectory
          with request(script_path) as response:
            # Create a temporary dir and store the script with the same name
            # as the URL's last part (instead of a random name).
            with TemporaryDirectory(delete = False) as tmpdir:
              from os.path import join, basename
              ctx.obj.tmpdir = tmpdir
              script_path = join(tmpdir, basename(urlparse(script_path).path))
              with open(script_path, 'wb') as f:
                f.write(response.read())

        # Remove -e/--exec and script_path from args
        new_args = args[:idx] + args[idx+2:]

        # Store the script path and remaining args in the context
        ctx.params['exec_file'] = script_path
        ctx.params['args'] = new_args

        return []  # No more arguments to process

    # Default processing for other cases
    return super().parse_args(ctx, args)

@click.group(cls=PassthroughCommand, invoke_without_command=True,
             context_settings=CONTEXT_SETTINGS)
@click.option('-e', '--exec', 'exec_file',
  type=click.Path(exists=True, dir_okay=False),
  help='Run the specified Python file with the CLI environment.')
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click.version_option(message='ocebuild-cli %(version)s', version=__version__)
@click.pass_context
def cli(ctx, exec_file=None, args=None):
  """Main runner for the CLI."""
  if exec_file and ctx.invoked_subcommand is None:
    try:
      # Run python script in a controlled namespace (inherits pyinstaller env)
      import runpy, sys

      sys.argv = [exec_file] + list(args) if args else [exec_file]
      ctx.obj.__dict__['argv'] = list(args) if args else []

      runpy.run_path(exec_file, run_name="__main__", init_globals=ctx.obj.__dict__)
      return
    # If an error occurs, abort with a message and traceback
    except Exception as e:
      abort(msg=f"Failed to execute {exec_file}: {e}", traceback=True)
    finally:
      tmpdir = ctx.obj.tmpdir
      if tmpdir:
        # Remove the temporary directory if it was created
        import tempfile
        from os.path import isdir
        from shutil import rmtree
        if isdir(tmpdir) and tmpdir.startswith(tempfile.gettempdir()):
          try:
            rmtree(tmpdir)
          except OSError as e:
            abort(msg=f"Failed to remove temporary directory {tmpdir}: {e}")

def cli_exit(env: Optional[CLIEnv]=None, status: int=0):
  """Cleanup the CLI environment on exit."""

  # Attempt to get the CLI environment from the current context.
  if not env and (ctx := click.get_current_context(silent=True)):
    env = ctx.find_object(CLIEnv) if ctx else None

  clear_cache([UNPACK_DIR])
  os_exit(status)

@cli.result_callback(replace=True)
@click.make_pass_decorator(CLIEnv)
def cli_exit_hook(env, res, status: int=0, **_):
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
    cli_exit(status=int(e.code) if e.code is not None else 0)
  # Catch any unhandled exceptions.
  except Exception: #pylint: disable=broad-exception-caught
    issues_url = _format_url("https://github.com/Qonfused/OCE-Build/issues")
    abort(msg="An unexpected error occurred.",
          hint=f"Please report this issue at {issues_url}.")

if __name__ == '__main__': _main()
