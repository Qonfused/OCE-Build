## @file
# Helper functions for parsing and executing Regex patterns.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

import re

from typing import Tuple, Union


def re_match(pattern, string, group:int=0) -> Union[Tuple[str], None]:
  """Match for a pattern in a string."""
  if (match := re.match(pattern, string)):
    return match.group(group)
  return None

def re_search(pattern, string, group:int=0) -> Union[Tuple[str], None]:
  """Search for a pattern in a string."""
  if (match := re.search(pattern, string)):
    return match.group(group)
  return None
