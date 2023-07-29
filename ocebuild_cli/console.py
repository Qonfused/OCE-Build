## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""CLI Console Utilities."""

from datetime import datetime
from functools import partial

from typing import List

import click
from rich.console import Console
from rich.text import Text
from rich.theme import Theme

from ocebuild.errors._lib import wrap_exception


START_TIME = datetime.now()
"""The start time of the CLI."""

LOGGING_THEME = {
  "logging.level.debug":    "dim",
  "logging.level.info":     "blue",
  "logging.level.success":  "green",
  "logging.level.error":    "red",
}

def _format_time(log_time: datetime) -> Text:
  """Renders a datetime object as a relative duration string."""
  seconds = (log_time - START_TIME).total_seconds()
  duration = datetime.utcfromtimestamp(seconds)
  return Text(duration.strftime('%Mm %Ss'))

console_wrapper = partial(Console,
                          theme=Theme(LOGGING_THEME),
                          log_path=False,
                          log_time_format=_format_time)
"""A wrapper for initializing a rich.console Console class instance."""

CONSOLE = console_wrapper()
"""A shared rich.console Console class instance.
@internal - This is a mutable constant that cannot be imported directly.
"""

def traceback_wrapper(suppress: List[any], **kwargs):
  """Wraps exception traceback frames and formats a traceback with rich."""
  if not suppress: suppress = []
  wrap_exception(suppress=[__file__, *suppress],
                 hide_modules=[click],
                 use_rich=True,
                 **kwargs)


__all__ = [
  # Constants (2)
  "START_TIME",
  "LOGGING_THEME",
  # Variables (1)
  "console_wrapper",
  # Functions (1)
  "traceback_wrapper"
]
