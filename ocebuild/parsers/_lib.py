## @file
# Parser helper functions.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##


def update_cursor(level: int,
                  key: str,
                  cursor: dict
                  ) -> None:
  """Updates the cursor dictionary.

  Args:
    level (int): The level of the cursor.
    key (str): The key of the cursor.
    cursor (dict): The cursor dictionary.
  """
  # Handle key (cursor) resets
  if level < 2: cursor['keys'] = [key]
  # Handle key (cursor) movement
  else:
    if level == cursor['level'] and len(cursor['keys']):
      cursor['keys'].pop(-1)
    elif level < cursor['level']:
      uplevel = (cursor['level'] - level) / cursor['indent']
      cursor['keys'].pop(-int(uplevel))
    cursor['keys'].append(key)
  # Update cursor
  cursor['level'] = level
  cursor['indent'] = level / max(1, len(cursor['keys']))
