## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Parser helper functions."""


def update_cursor(level: int,
                  key: str,
                  cursor: dict,
                  upshift: int=0,
                  ) -> None:
  """Updates the cursor dictionary.

  Args:
    level: The level of the cursor.
    key: The key of the cursor.
    cursor: The cursor dictionary.
    uplevel: Number of levels to ignore
  """
  bias = cursor['indent'] if upshift else 1
  # Handle key (cursor) resets
  if level < 2: cursor['keys'] = [key]
  # Handle key (cursor) movement
  else:
    if level == cursor['level'] and len(cursor['keys']):
      cursor['keys'].pop(-1)
    elif cursor['keys'] and level < cursor['level']:
      downlevel = (cursor['level'] - level) / cursor['indent']
      cursor['keys'] = cursor['keys'][:-int(downlevel + upshift)]
    cursor['keys'].append(key)
  # Update cursor
  cursor['level'] = level
  cursor['indent'] = max(bias, level / max(1,(len(cursor['keys']) - upshift)))


__all__ = [
  "update_cursor"
]
