## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Parser helper functions."""

from copy import deepcopy

from typing import List

from .regex import re_search


TAGS = ('@append', '@delete', '@fallback', '@override', '@prepend')
"""Preprocessor tags for controlling output dict semantics."""

def _append_tags(cursor: dict,
                 frontmatter_dict: dict,
                 defer_tree: bool=False
                 ) -> None:
  """Append tag to frontmatter if entries marked with tag.

  Args:
    cursor: The cursor dictionary.
    frontmatter_dict: The frontmatter dictionary.
    defer_tree: Whether to defer tree tag resolution until the next call.
  """

  if cursor['has_tag'] is None: return
  tag_name, tag_options = cursor['has_tag']

  # Leave tag tree null until another tag discovers the tree tag
  if defer_tree:
    if not 'defer_tree' in cursor: cursor['defer_tree'] = []
    cursor['defer_tree'].append(len(frontmatter_dict['tags']))
    tag_tree = None
  else:
    # Update deferred trees with current tree value
    if 'defer_tree' in cursor:
      for deferred in cursor['defer_tree']:
        frontmatter_dict['tags'][deferred][1] = deepcopy(cursor['tag_tree'])
      del cursor['defer_tree']
    tag_tree = deepcopy(cursor['tag_tree'])

  frontmatter_dict['tags'].append([tag_name, tag_tree, tag_options])
  # Reset cursor attr
  cursor['has_tag'] = None

def _apply_macro(macro: str,
                 flags: List[str],
                 cursor: dict,
                 frontmatter_dict: dict
                 ) -> None:
  """Applies preprocessor macros to parser cursor or frontmatter.

  Args:
    macro: The macro to apply.
    flags: The current flags.
    tokens: The parsed tokens.
    cursor: The cursor dictionary.
    frontmatter_dict: The frontmatter dictionary.
  """

  # Check if macro has flag
  flag = re_search(r'\((.*)\)', macro, group=1)
  if flag is not None: macro = macro[:-len(f'({flag})')]

  # Mark tagged entries on cursor (to append to frontmatter)
  if any(macro.startswith(t) for t in TAGS):
    # Handle any unresolved tags (non-attached)
    if cursor['has_tag'] is not None:
      _append_tags(cursor, frontmatter_dict, defer_tree=True)
    cursor['has_tag'] = (macro, flag)
  # Check if flag exists
  elif macro == '@ifdef':
    is_defined = (flag in flags) \
              or (flag in frontmatter_dict)
    cursor['skip'] = not is_defined
  elif macro == '@ifndef':
    is_not_defined = (flag not in flags) \
                  and (flag not in frontmatter_dict)
    cursor['skip'] = not is_not_defined
  # Check if flag meets conditional
  # elif macro == '@if':
  # elif macro == '@elif':
  # Switch macro skip
  elif macro == '@else':
    cursor['skip'] = not cursor['skip']
  # End macro checking scope
  elif macro == '@endif':
    cursor['skip'] = False

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
  # Constants (1)
  "TAGS",
  # Functions (1)
  "update_cursor"
]
