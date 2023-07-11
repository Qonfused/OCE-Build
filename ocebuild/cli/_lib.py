## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Shared CLI utilities."""

from functools import partial
from sys import exit as sys_exit

from typing import Iterator, List, Optional, Union

import click
from rich.progress import track


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
"""Shared context settings for the CLI."""

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
  if exit is not None: sys_exit(exit)

def error(msg: str, hint: Optional[str]=None) -> None:
  calls = [{ "msg": f"\nError: {msg}", "fg": "red" }]
  if hint: calls.append({ "msg": f"       {hint}" })
  echo(calls=calls, exit=1)

def progress_bar(description: str,
                 *args,
                 **kwargs
                 ) -> Iterator:
  """Stylized progress bar for the CLI."""
  return partial(track, description=description, *args, **kwargs)
