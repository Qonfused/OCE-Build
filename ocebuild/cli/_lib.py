## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Shared CLI utilities."""

import inspect
from functools import partial, wraps as functools_wraps
from sys import exit as sys_exit

from typing import Callable, Generator, Iterator, List, Optional, Union

import click
from rich.progress import Progress, track

from ocebuild.errors._lib import wrap_exception


CONTEXT_SETTINGS = { "help_option_names": ['-h', '--help'] }
"""Shared context settings for the CLI."""

################################################################################
#                            CLI Environment Utilities                         #
################################################################################

VERBOSE: bool=False
"""Global verbose flag for the CLI."""

DEBUG: bool=False
"""Global debug flag for the CLI."""

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
    global VERBOSE, DEBUG
    if name == 'verbose':
      VERBOSE = value
    elif name == 'debug':
      DEBUG = value
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
  """Formats a URL for the CLI.

  Args:
    url: The URL to format.

  Returns:
    A rich-formatted URL.
  """
  return click.style(url, fg="blue", underline=True, bold=True)

def debug(msg: str, *args, **kwargs):
  """Prints a debug message.

  This function is a wrapper for `echo()` that only prints if the global
  `DEBUG` flag is set.

  Args:
    msg: The message to print.
    *args: Additional arguments to pass to `echo()`.
    **kwargs: Additional keyword arguments to pass to `echo()`.

  Example:
    >>> debug('This is a debug message.')
    # -> DEBUG: This is a debug message.
  """
  if not DEBUG: return
  echo(msg=f"DEBUG: {msg}", *args, dim=True, **kwargs)

def echo(msg: Optional[str]=None,
         *args,
         calls: Optional[List[Union[str, dict]]]=None,
         exit: Optional[int]=None, #pylint: disable=redefined-builtin
         **kwargs
         ) -> None:
  """Stylized echo for the CLI.

  Args:
    msg: The message to print.
    *args: Additional arguments to pass to `click.echo()`.
    calls: A list of additional calls to `echo()`.
    exit: The exit code to exit with. (Optional)
    **kwargs: Additional keyword arguments to pass to `click.echo()`.

  Example:
    >>> echo('This is a message.')
    # -> This is a message.
  """
  if msg:
    click.echo(click.style(msg, *args, **kwargs))
  elif calls:
    for call in calls:
      if isinstance(call, dict):
        echo(*args, **call, **kwargs)
      elif isinstance(call, str):
        echo(msg=call, *args, **kwargs)
  if exit is not None:
    sys_exit(exit)

def error(msg: str,
          label: str='Error',
          hint: Optional[str]=None,
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

  header = click.style(f'{label}: ', fg="red", bold=True)
  calls = [{ "msg": f"\n{header}{msg}", "fg": "red" }]
  if hint:
    padding = ' ' * len(f'{label}: ')
    calls.append({ "msg": f"{padding}{hint}" })
  calls[-1]['msg'] += '\n'
  echo(calls=calls)

  # Wrap the public traceback frames if specified
  if traceback:
    if not suppress: suppress = []
    wrap_exception(suppress=[__file__, *suppress],
                   hide_modules=[click],
                   use_rich=True)

  sys_exit(1)

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
  error(msg, 'Abort', hint, traceback, suppress=[caller])

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
  # Functions (6)
  "cli_command",
  "debug",
  "echo",
  "error",
  "abort",
  "progress_bar",
  # Classes (1)
  "CLIEnv"
]
