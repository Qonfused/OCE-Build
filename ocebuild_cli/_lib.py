## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Shared CLI utilities."""

from functools import wraps as functools_wraps

from typing import Optional

import click


CONTEXT_SETTINGS = { "help_option_names": ['-h', '--help'] }
"""Shared context settings for the CLI."""

VERBOSE = False
"""Global verbose flag for the CLI.
@internal - This is a mutable constant that cannot be imported directly.
"""

DEBUG = False
"""Global debug flag for the CLI.
@internal - This is a mutable constant that cannot be imported directly.
"""

class CLIEnv:
  """Shared CLI environment."""

  global VERBOSE, DEBUG
  def __init__(self,
               verbose_flag: bool=VERBOSE,
               debug_flag: bool=DEBUG):
    self.verbose = verbose_flag
    self.debug = debug_flag

  def __setattr__(self, name: str, value: any) -> None:
    """Sets an attribute on the CLI environment."""
    global VERBOSE, DEBUG, Console
    if name == 'verbose':
      VERBOSE = value
    elif name == 'debug':
      DEBUG = value
      #pylint: disable=import-outside-toplevel
      import ocebuild_cli.console as Console
      Console.CONSOLE = Console.console_wrapper(log_path=value)
    super().__setattr__(name, value)

def cli_command(name: Optional[str]=None):
  """Factory for creating a shared environment for CLI commands.

  Args:
    name: The name of the command. Defaults to the function name.

  Returns:
    A decorator for passing the CLI environment to commands.

  Example:
    >>> @cli_command()
    ... def cli(env, *args, **kwargs):
    ...   print(env)
    # -> <ocebuild.cli._lib.CLIEnv object at 0x108bf73d0>
  """
  def cli_wrapper(func):
    """Decorator for passing the CLI environment to commands."""
    nonlocal name
    @click.command(name=name or func.__name__)
    @click.option('-v', '--verbose',
                  is_flag=True,
                  help='Enable verbose output.')
    @click.option('--debug',
                  is_flag=True,
                  help='Enable debug output.')
    @click.make_pass_decorator(CLIEnv)
    @functools_wraps(func)
    def _command_wrapper(env: CLIEnv,
                         *args,
                         verbose: bool,
                         debug: bool,
                         **kwargs):
      """Simple environment wrapper for CLI commands."""
      _rich_traceback_omit = True #pylint: disable=invalid-name,unused-variable

      # Set the global verbose and debug flags.
      env.verbose = verbose
      env.debug = debug

      # Note the entrypoint of the CLI command.
      if debug:
        from third_party.cpython.pathlib import Path
        from .logging import debug as debug_log
        entrypoint = Path(__file__).with_name('__main__.py')
        debug_log(f"Launching CLI from {entrypoint}.")

      return func(env, *args, **kwargs)
    return _command_wrapper
  return cli_wrapper


__all__ = [
  # Constants (1)
  "CONTEXT_SETTINGS",
  # Functions (1)
  "cli_command",
  # Classes (1)
  "CLIEnv"
]
