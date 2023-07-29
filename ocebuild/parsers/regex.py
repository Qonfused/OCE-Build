## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Helper functions for parsing and executing Regex patterns."""

import re
from re import MULTILINE as flag_multiline

from typing import Callable, Tuple, Union


def _wrap_module(module: Callable,
                 pattern,
                 string,
                 group: int=0,
                 multiline: bool=False
                 ) -> Union[Tuple[str], None]:
  """Wraps a regex module with additional options."""
  if not multiline: flags = 0
  else: flags = flag_multiline
  # Return match
  if (match := module(pattern, string, flags=flags)):
    if group is None: return match
    return match.group(group)
  return None

def re_match(pattern,
             string,
             group: int=0,
             multiline: bool=False
             ) -> Union[Tuple[str], None]:
  """Match for a pattern in a string."""
  return _wrap_module(re.match, pattern, string, group, multiline)

def re_search(pattern,
              string,
              group:int=0,
              multiline: bool=False
              ) -> Union[Tuple[str], None]:
  """Search for a pattern in a string."""
  return _wrap_module(re.search, pattern, string, group, multiline)


__all__ = [
  # Functions (2)
  "re_match",
  "re_search"
]
