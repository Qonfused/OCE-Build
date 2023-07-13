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


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
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
               verbose: bool=VERBOSE,
               debug: bool=DEBUG):
    self.verbose = verbose
    self.debug = debug

  def __setattr__(self, __name: str, __value: any) -> None:
    """Sets an attribute on the CLI environment."""
    global VERBOSE, DEBUG
    if   __name == 'verbose': VERBOSE = __value
    elif __name == 'debug': DEBUG = __value
    super().__setattr__(__name, __value)

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
                          verbose: bool,
                          debug: bool,
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
  return click.style(url, fg="blue", underline=True, bold=True)

def debug(msg: str, *args, **kwargs):
  """Prints a debug message."""
  global DEBUG
  if not DEBUG: return
  echo(msg=f"DEBUG: {msg}", *args, dim=True, **kwargs)

def echo(msg: Optional[str]=None,
         *args,
         calls: Optional[List[Union[str, dict]]]=None,
         exit: Optional[int]=None,
         **kwargs
         ) -> None:
  """Stylized echo for the CLI."""
  if msg:
    click.echo(click.style(msg, *args, **kwargs))
  elif calls:
    for call in calls:
      if   isinstance(call, dict):  echo(*args, **call, **kwargs)
      elif isinstance(call, str):   echo(msg=call, *args, **kwargs)
  if exit is not None:
    sys_exit(exit)

def error(msg: str,
          label: str='Error',
          hint: Optional[str]=None,
          traceback: bool=False,
          suppress: Optional[List[str]]=None
          ) -> None:
  """Stylized error message for the CLI."""

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

def abort(msg: str, hint: Optional[str]=None) -> None:
  caller = inspect.stack()[1].filename
  error(msg=msg, hint=hint, label='Abort', traceback=True, suppress=[caller])

################################################################################
#                           CLI Interactive Utilities                          #
################################################################################

def progress_bar(description: str,
                 *args,
                 wrap: Callable=track,
                 **kwargs
                 ) -> Generator[Iterator, any, None]:
  """Stylized progress bar for the CLI."""
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
