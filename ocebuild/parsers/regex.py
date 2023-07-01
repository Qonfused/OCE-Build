## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Helper functions for parsing and executing Regex patterns."""

import re
from re import MULTILINE as flag_multiline

from typing import Tuple, Union


def re_match(pattern, string,
             group: int=0,
             multiline: bool=False
             ) -> Union[Tuple[str], None]:
  """Match for a pattern in a string."""
  if not multiline: flags = 0
  else: flags = flag_multiline
  # Return match
  if (match := re.match(pattern, string, flags=flags)):
    return match.group(group)
  return None

def re_search(pattern, string,
              group:int=0,
              multiline: bool=False
              ) -> Union[Tuple[str], None]:
  """Search for a pattern in a string."""
  if not multiline: flags = 0
  else: flags = flag_multiline
  # Return match
  if (match := re.search(pattern, string, flags=flags)):
    return match.group(group)
  return None

__all__ = [
  "re_match",
  "re_search"
]
