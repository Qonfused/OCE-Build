## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""CLI Logging Utilities."""

#TODO: Refactor to use the native logging hook
# @see https://rich.readthedocs.io/en/stable/logging.html

import inspect
from functools import partial

from typing import List, Optional

from ocebuild.parsers.dict import nested_get

import ocebuild_cli._lib as lib
import ocebuild_cli.console as Console
from ocebuild_cli.console import traceback_wrapper, LOGGING_THEME


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
    indent = ' ' * (len(label) + 2)
    fmt_msg += f"\n{indent}{padding}{hint}"
  return fmt_msg

def echo(msg: str='', *args, log: bool=True, **kwargs) -> None:
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
    fn = partial(Console.CONSOLE.log, _stack_offset=3)
  else:
    fn = Console.CONSOLE.print
  fn(msg, *args, markup=True, **kwargs)

################################################################################
#                              CLI Logging Utilities                           #
################################################################################

def debug(msg: str, *args, **kwargs):
  """Prints a debug message.

  This function is a wrapper for `echo()` that only prints if the global
  `DEBUG` flag is set.
  """
  if lib.DEBUG:
    echo(_format_label(f"[dim]{msg}[/dim]", 'DEBUG'), *args, log=True, **kwargs)

def info(msg: str, *args, **kwargs):
  """Prints an info message.

  This function is a wrapper for `echo()` that only prints if the global
  `VERBOSE` flag is set.
  """
  if lib.VERBOSE:
    echo(_format_label(msg, 'INFO'), *args, log=True, **kwargs)

def success(msg: str, *args, **kwargs):
  """Prints a success message."""
  echo(_format_label(msg, 'SUCCESS'), *args, log=True, **kwargs)

def error(msg: str,
          hint: Optional[str]=None,
          label: str='ERROR',
          traceback: bool=False,
          suppress: Optional[List[str]]=None,
          hide_locals: bool=True,
          **kwargs
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
  color = nested_get(LOGGING_THEME, [f"logging.level.error"])
  echo(_format_label(msg, label, color, hint), log=True, **kwargs)

  # Wrap the public traceback frames if specified
  if traceback:
    traceback_wrapper(suppress=suppress, hide_locals=hide_locals)

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
  error(msg, hint, 'ABORT', traceback, suppress=[caller],
        hide_locals=True,
        _stack_offset=4)


__all__ = [
  # Functions (6)
  "echo",
  "debug",
  "info",
  "success",
  "error",
  "abort"
]
