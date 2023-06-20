## @file
# Parser for converting property list to a Python dictionary.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

import re
from base64 import b64encode, b64decode
from dateutil.parser import parse

from parsers._lib import _updateCursor
from parsers.dict import flattenDict, nestedGet, nestedSet


plist_schema = {
  '1.0': [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">',
    '<plist version="1.0">',
    '<dict>',
    '</dict>',
    '</plist>'
  ]
}

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

def writeSerializedTypes(value, defaults=('dict', None)):
  # Extract native type and value
  stype, svalue = defaults
  if svalue is not None:
    stype  = value[0] if isinstance(value, tuple) else 'string'
    svalue = value[1] if isinstance(value, tuple) else ''
    # Handle empty entries
    try:
      if not len(svalue):
        if type(svalue) == dict: stype = 'dict'
        if type(svalue) == list: stype = 'array'
    except: pass
  entry  = None
  match stype:
    case 'date':    pass
    case 'string':  pass
    # Handle alternate serialized types
    case 'float':   stype = 'real'
    case 'int':     stype = 'integer'
    # Handle alternate serialized values
    case 'data':    svalue = b64encode(bytes.fromhex(svalue)).decode()
    # Handle alternate entry schemas
    case 'bool':
      entry = [f'<{(stype := str(svalue).lower())}/>']
    case _:
      entry = [f'<{stype}>', f'</{stype}>']
  # Default entry schema
  if entry is None:
    entry = [f'<{stype}>{svalue}</{stype}>']
  return entry

def parsePlist(lines: list[str],
               config: dict=dict()):
  """Parses a property list into a Python dictionary.

  Args:
    lines: Property list (plist) lines.
    config: Dictionary to be populated.

  Returns:
    Dictionary populated from plist entries.
  """
  cursor = { 'keys': [], 'level': 0, 'indent': 0, 'skip': (def_flag := False) }
  for i,line in enumerate(lines):
    # Skip empty lines
    if len(lnorm := line.lstrip()) == 0:
      continue
    # Skip multiline comments
    if lnorm.startswith('<!--') or (__comment_end := lnorm.endswith('-->')):
      cursor['skip'] = __comment_end
      continue
    if cursor['skip']:
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
      # Attempt single-line extraction of type and value
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

def writePlist(lines: list[str]=plist_schema['1.0'],
               config: dict=dict()):
  """Writes a property list from a Python dictionary.

  Args:
    lines: Property list (plist) lines.
    config: Dictionary to be written.

  Returns:
    Property list (plist) lines.
  """
  def try_index(*args):
    try: return lines.index(*args)
    except: return -1
  cursor = { 'line': 0, 'indent': 2 }
  for (keys, value) in flattenDict(config).items():
    # Validate root dicitonary entry
    head = try_index('<dict>')
    if head == -1: raise Exception(f'Invalid property list: No root found.')

    # Seek or create head index for current tree level
    for j, key in enumerate(tree := str(keys).split('.')):
      padding = (" "*cursor['indent'])*(j+1)

      # Create parent dictionary for object arrays
      is_root_key = (j == len(tree)-1)
      if isinstance(key, int):
        # Seek to current array index
        num_entries = 0
        while not (has_array_index := key == (num_entries - 1)):
          line_padding = (line := lines[head])[:-len(line.lstrip())]
          if line == f'{padding[:-2]}</array>': break
          elif line == f'{line_padding}<dict>': num_entries += 1
          head += 1
        # Skip end of previous array entry
        if (has_entries := lines[head-1] != f'{padding[:-2]}<array>'):
          while lines[head-1] != f'{padding}</dict>': head += 1
          head -= 1
        # Create new array entry
        if not (has_entries and has_array_index):
          if has_entries: head += 1
          lines[head:head] = [f'{padding}<dict>', f'{padding}</dict>']
          head += 1
        # Seek to end of entry
        continue
      # Insert array indices as additional keys
      elif (re_match := re.search('(.*)\[([0-9]+)\]', key)):
        key, idx = re_match.groups()
        tree[j] = key
        tree[j+1:j+1] = [int(idx)]
      
      # Search for key in current level
      key_ln = f'{padding}<key>{key}</key>'
      match (index := try_index(key_ln, head)):
        # Create a new key
        case -1:
          # Always append to end of dictionary
          if not lines[head].lstrip().startswith('</dict>'):
            while not lines[head-1].startswith(f'{padding}</'):
              head += 1
              if lines[head].startswith(f'{padding}<key>'): head += 1
              if lines[head].startswith(f'{padding[:-2]}</'): break
          # Append new entry
          defaults = ('dict' if not re_match else 'array', '' if is_root_key else None)
          lns = [f'{padding}{v}' for v in writeSerializedTypes(value, defaults)]
          lines[head:head] = (entry := [key_ln, *lns])
          head += len(entry) - 1
        # Seek end of level
        case _:
          if index >= head: head = index + 1
          for line in lines[head:]:
            if len(padding) < len(line[:-len(line.lstrip())]): head += 1
            else: break
          head += 1

  return lines
