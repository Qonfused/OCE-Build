## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Shared CLI utilities."""

from functools import partial
from sys import exit as sys_exit

from typing import Callable, Generator, Iterator, List, Optional, Union

import click
from rich.progress import Progress, track

from ocebuild import __file__
from ocebuild.errors._lib import wrap_exception


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
"""Shared context settings for the CLI."""

def _format_url(url: str) -> str:
  return click.style(url, fg="blue", underline=True, bold=True)

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
    wrap_exception(suppress=[click, __file__, *suppress],
                   use_rich=True)
  
  sys_exit(1)

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
