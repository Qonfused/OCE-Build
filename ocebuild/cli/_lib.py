## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Shared CLI utilities."""

import inspect
from functools import partial, wraps as functools_wraps

from typing import Callable, Generator, Iterator, List, Optional

import click
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, track
from rich.theme import Theme

from ocebuild.errors._lib import wrap_exception
from ocebuild.parsers.dict import nested_get


CONTEXT_SETTINGS = { "help_option_names": ['-h', '--help'] }
"""Shared context settings for the CLI."""

LOGGING_THEME = {
  "logging.level.debug":    "dim",
  "logging.level.info":     "blue",
  "logging.level.success":  "green",
  "logging.level.error":    "red",
}

console_wrapper = partial(Console,
                          theme=Theme(LOGGING_THEME),
                          log_path=False)
"""A wrapper for the rich.console Console class instance.
@internal
"""

################################################################################
#                            CLI Environment Utilities                         #
################################################################################

VERBOSE: bool=False
"""Global verbose flag for the CLI."""

DEBUG: bool=False
"""Global debug flag for the CLI."""

console = console_wrapper()
"""A shared rich.console Console class instance.
@internal
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
    global VERBOSE, DEBUG, console
    if name == 'verbose':
      VERBOSE = value
    elif name == 'debug':
      DEBUG = value
      console = console_wrapper(log_path=value)
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
    @click.command(name=name if name else func.__name__)
    @click.option('-v', '--verbose',
                  is_flag=True,
                  help='Enable verbose output.')
    @click.option('--debug',
                  is_flag=True,
                  help='Enable debug output.')
    @click.make_pass_decorator(CLIEnv)
    @functools_wraps(func)
    def _command_wrapper(env:CLIEnv,
                         *args,
                         verbose: bool, #pylint: disable=redefined-outer-name
                         debug: bool,   #pylint: disable=redefined-outer-name
                         **kwargs):
      """Simple environment wrapper for CLI commands."""
      env.verbose = verbose
      env.debug = debug
      return func(env, *args, **kwargs)
    return _command_wrapper
  return cli_wrapper

################################################################################
#                              CLI Output Utilities                            #
################################################################################

def _format_url(url: str) -> str:
  """Formats a URL for the CLI."""
  return f'[bold][link={url}]{url}[/link][/bold]'

def _format_label(msg: str,
                  label: str,
                  color: Optional[str]=None,
                  hint: Optional[str]=None,
                  ) -> str:
  """Formats a multi-line labeled message for the CLI."""
  color = nested_get(LOGGING_THEME, [f"logging.level.{label.lower()}"],
                     default=color)
  padding = " " * (8 - len(label))
  fmt_msg = f"[{color}][bold]{label}[/bold]: {padding}[/{color}]{msg}"
  if hint:
    indent = ' ' * len(label) + 2
    fmt_msg += f"\n{indent}{padding}{hint}"
  return fmt_msg

def echo(msg: str, *args, log: bool=True, **kwargs) -> None:
  """Stylized echo for the CLI.

  Args:
    msg: The message to print.
    *args: Additional arguments to pass to `console.print()`.
    **kwargs: Additional keyword arguments to pass to `console.print()`.

  Example:
    >>> echo('This is a message.')
    # -> This is a message.
  """
  if log:
    fn = partial(console.log, _stack_offset=3)
  else:
    fn = console.print
  fn(msg, *args, markup=True, **kwargs)

def traceback_wrapper(suppress: List[any]):
  """Wraps exception traceback frames and formats a traceback with rich."""
  if not suppress: suppress = []
  wrap_exception(suppress=[__file__, *suppress],
                 hide_modules=[click],
                 use_rich=True)

################################################################################
#                              CLI Logging Utilities                           #
################################################################################

#TODO: Refactor to use the native logging hook
# @see https://rich.readthedocs.io/en/stable/logging.html

def debug(msg: str, *args, **kwargs):
  """Prints a debug message.

  This function is a wrapper for `echo()` that only prints if the global
  `DEBUG` flag is set.
  """
  if DEBUG:
    echo(_format_label(msg, 'DEBUG'), *args, log=True, **kwargs)

def info(msg: str, *args, **kwargs):
  """Prints an info message.

  This function is a wrapper for `echo()` that only prints if the global
  `VERBOSE` flag is set.
  """
  if VERBOSE:
    echo(_format_label(msg, 'INFO'), *args, log=True, **kwargs)

def success(msg: str, *args, **kwargs):
  """Prints a success message."""
  echo(_format_label(msg, 'SUCCESS'), *args, log=True, **kwargs)

def error(msg: str,
          hint: Optional[str]=None,
          label: str='Error',
          traceback: bool=False,
          suppress: Optional[List[str]]=None
          ) -> None:
  """Stylized error message for the CLI.

  Args:
    msg: The error message to print.
    label: The label to print before the error message.
    hint: A hint to print after the error message. (Optional)
    traceback: Whether to print a traceback. (Optional)
    suppress: A list of filepaths to suppress from the traceback. (Optional)

  Example:
    >>> error('This is an error message.')
    # -> Error: This is an error message.
  """
  echo(_format_label(msg, label, hint=hint), log=True)

  # Wrap the public traceback frames if specified
  if traceback:
    traceback_wrapper(suppress=suppress)

def abort(msg: str,
          hint: Optional[str]=None,
          traceback: bool=True
          ) -> None:
  """Stylized abort message for the CLI.

  This function is a wrapper for `error()` that exits with a non-zero exit code.
  By default, a full traceback is printed using `wrap_exception()`, hiding
  internal stack frames.

  Args:
    msg: The abort message to print.
    hint: A hint to print after the abort message. (Optional)
    traceback: Whether to print a traceback; enabled by default. (Optional)

  Example:
    >>> abort('This is an abort message.')
    # -> Abort: This is an abort message.
    # (rich.console `print_exception()` traceback)
  """
  caller = inspect.stack()[1].filename
  error(msg, hint, 'Abort', traceback, suppress=[caller])

################################################################################
#                           CLI Interactive Utilities                          #
################################################################################

def progress_bar(description: str,
                 *args,
                 wrap: Callable=track,
                 **kwargs
                 ) -> Generator[Iterator, any, None]:
  """Stylized progress bar for the CLI.

  Args:
    description: The description to display for the progress bar.
    *args: Additional arguments to pass to `rich.track()`.
    wrap: The function to wrap the progress bar with. (Optional)
      This can be a parent rich.Progress() context, or a custom wrapper.
    **kwargs: Additional keyword arguments to pass to `rich.track()`.

  Returns:
    A partial for a generator that yields an iterator for the progress bar.
  """
  if isinstance(wrap, Progress):
    ctx = wrap
    task_id = ctx.add_task(description, total=None)
    ctx.start_task(task_id)
    kwargs['task_id'] = task_id
    wrap = ctx.track
  return partial(wrap, description=description, *args, **kwargs)


__all__ = [
  # Constants (1)
  "CONTEXT_SETTINGS",
  # Functions (9)
  "cli_command",
  "echo",
  "traceback_wrapper",
  "debug",
  "info",
  "success",
  "error",
  "abort",
  "progress_bar",
  # Classes (1)
  "CLIEnv"
]
