## @file
# Parser for converting property list to a Python dictionary.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

import re
from base64 import b64decode
from dateutil.parser import parse

from parsers._lib import _updateCursor
from parsers.dict import nestedGet, nestedSet


def parseSerializedTypes(stype: str, value: str):
  """Parse property list types to Python types.

  Args:
    stype: Property list type.
    value: Property list value.

  Returns:
    Tuple of (type, value) for the given type.
  """
  entry = None
  try:
    match stype:
      case 'array':   entry = []
      case 'data':    entry = (stype, b64decode(value).hex().upper())
      case 'date':    entry = (stype, parse(value, fuzzy=True))
      case 'dict':    entry = {}
      case 'real':    entry = ('float', float(value))
      case 'integer': entry = ('int', int(value))
      case 'string':  entry = (stype, value)
      case 'true':    entry = ('bool', True)
      case 'false':   entry = ('bool', False)
  except: pass # De-op
  return entry

def parsePlist(lines: list[str],
               config: dict=dict()):
  """Parses a property list into a Python dictionary.

  Args:
    lines: property list (plist) lines.
    config: Dictionary to be populated.

  Returns:
    Dictionary populated from plist entries.
  """
  cursor = { 'keys': [], 'level': 0, 'indent': 0, 'skip': (def_flag := True) }
  for i,line in enumerate(lines):
    # Skip empty lines
    if len(lnorm := line.lstrip()) == 0:
      continue
    # Skip multiline comments
    if lnorm.startswith('<!--') or (__comment_end := lnorm.endswith('-->')):
      cursor['skip'] = not __comment_end
      continue
    if not cursor['skip']:
      continue

    level = len(line[:-len(lnorm)])
    # Skip root or closing properties
    if lnorm.startswith('</') or level == 0: continue

    # Update cursor position
    if (lnorm := lnorm.rstrip()).endswith('</key>'):
      key = lnorm[len('<key>'):-len('</key>')]
      _updateCursor(level, key, cursor)
    # Update dictionary values
    elif lnorm.startswith('<'):
      stype = re.findall('<([a-z]+)\/?>', lnorm, re.IGNORECASE)[0]
      value = re.findall('<[a-z]+>(.*)</[a-z]+>', lnorm, re.IGNORECASE)
      if len(value): value = value[0]

      # Extract and validate parent tree level
      tree = cursor['keys']
      while len(tree)-1 >= level / max(1, cursor['indent']):
        cursor['level'] -= cursor['indent']
        # Handle object arrays separately
        if lines[i-1].lstrip().startswith(f'</{stype}>'):
          tree.pop(-1)
        # Handle dictionary keys separately
        else:
          tree.pop(-2)
      
      # Parse property list types to Python types
      # @see https://www.apple.com/DTDs/PropertyList-1.0.dtd
      entry = parseSerializedTypes(stype, value)
      if entry is None: continue

      # Handle object and array traversal
      ptree = tree[:-1] if stype != 'dict' else tree
      prev_value = nestedGet(config, ptree)
      match prev_value:
        case dict() | None:
          nestedSet(config, tree, entry)
        case list():
          match stype:
            # Always append dictionaries to arrays
            case 'dict':
              prev_value.append(entry)
              nestedSet(config, ptree, prev_value)
            # Add new key to last dictionary in array
            case _:
              *tree, key = tree
              prev_value[-1][key] = entry
              nestedSet(config, tree, prev_value)
    # Reached invalid line
    else: raise Exception(f'Invalid line at position {i}:\n\n{line}')

  return config
