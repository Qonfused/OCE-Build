## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Stacktrace introspection methods used for testing and at runtime."""

import sys
from contextlib import contextmanager
from sys import exc_info
from traceback import extract_tb, print_exception

from typing import List, Optional

from ocebuild import __file__


@contextmanager
def disable_exception_traceback(tracebacklimit: int=0):
  """Suppresses stack trace information from an exception.
  
  Args:
    tracebacklimit: The number of stack frames to show. Defaults to 0.

  Example:
    >>> with disable_exception_traceback():
    ...   raise Exception('This exception will not show a stack trace.')
    # -> Exception: This exception will not show a stack trace.
  """
  default_value = sys.__dict__.get('tracebacklimit', 1000)
  sys.tracebacklimit = tracebacklimit
  yield
  sys.tracebacklimit = default_value

def wrap_exception(suppress: Optional[List[str]]=None,
                   suppress_internal: bool=True,
                   suppress_stdlib: bool=False,
                   hide_suppressed: bool=True,
                   max_frames: int=100,
                   use_rich: bool=False):
  """Hides internal stackframes with an optional stylized stack trace.
  
  Args:
    suppress: A list of paths to suppress from the stack trace.
    suppress_internal: Whether to suppress internal frames (default: True).
    suppress_stdlib: Whether to suppress standard library frames (default: False).
    hide_suppressed: Whether to hide suppressed frames (default: True).
    max_frames: The maximum number of frames to show (default: 100).
    use_rich: Whether to use rich to display the stack trace (default: False).

  Example:
    >>> try:
    ...   raise Exception('This exception will not show internal frames.')
    ... except Exception:
    ...   wrap_exception()
    # -> Exception: This exception will not show internal frames.
  """
  if not suppress: suppress = []
  e_type, e, tb = exc_info()

  # Delayed import to avoid circular dependency
  from ocebuild.sources.resolver import PathResolver
  __module = str(PathResolver(__file__).parent)

  tb_frame = tb
  tb_prev = None
  prev_frame = None
  excluded_paths = [__file__, *suppress]
  for frame in extract_tb(tb, limit=None):
    # Stop at the end of the traceback
    if not tb_frame: break
    # Don't include internal frames (if specified)
    is_internal_frame = \
      suppress_internal and frame.name.startswith('_')
    # Don't include duplicate frames
    is_duplicate_frame = False
    if prev_frame:
      is_duplicate_frame = \
        prev_frame.filename == frame.filename and \
        prev_frame.lineno == frame.lineno and \
        prev_frame.name == frame.name

    # Don't include internal methods when suppressed
    if is_internal_frame or is_duplicate_frame:
      if tb_prev: tb_prev.tb_next = None
    elif suppress_stdlib and not __module in (path := frame.filename):
      excluded_paths.append(path)
    elif hide_suppressed:
      if tb_prev: tb_prev.tb_next = tb_frame
      tb_prev = tb_frame
    tb_frame = tb_frame.tb_next
    prev_frame = frame
  
  if use_rich:
    _rich_traceback_omit = True
    from rich.console import Console
    Console().print_exception(show_locals=True,
                              suppress=excluded_paths,
                              max_frames=max_frames)
  else:
    print_exception(e_type, e, tb, limit=max_frames, file=sys.stdout)


__all__ = [
  # Functions (2)
  "disable_exception_traceback",
  "wrap_exception"
]
