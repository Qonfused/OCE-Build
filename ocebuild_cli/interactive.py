## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""CLI Interactive Utilities."""

from datetime import datetime
from functools import partial

from typing import Callable, Generator, Iterator

from rich.progress import Progress as rich_progress, track
from rich.table import Table

import ocebuild_cli.console as Console
from ocebuild_cli.console import _format_time


class log_progress(rich_progress):
  """An extended rich.progress.Progress class for the CLI."""
  def get_renderables(self):
    """Renders the progress bar into a `console.log` aligned table"""
    time = _format_time(datetime.now())
    renderable = self.make_tasks_table(self.tasks)
    # Construct grid
    grid = Table.grid(expand=False)
    grid.add_column(no_wrap=True, min_width=len(time) + 1)
    grid.add_column(no_wrap=True)
    grid.add_row(f"[cyan]{time}[/cyan]", renderable)
    yield grid

Progress = partial(log_progress, console=Console.CONSOLE)
"""A customized `log_progress` class wrapper."""

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
  if isinstance(wrap, rich_progress):
    ctx = wrap
    task_id = ctx.add_task(description, total=None)
    ctx.start_task(task_id)
    kwargs['task_id'] = task_id
    wrap = ctx.track
  return partial(wrap, description=description, *args, **kwargs)


__all__ = [
  # Variables (1)
  "Progress",
  # Functions (1)
  "progress_bar",
  # Classes (1)
  "log_progress"
]
