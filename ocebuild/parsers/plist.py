## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Parser for converting property list to a Python dictionary."""

from base64 import b64encode, b64decode
from datetime import datetime
from io import TextIOWrapper
import re
from typing import List, Optional, Tuple, Union

from ocebuild.parsers._lib import update_cursor
from ocebuild.parsers.dict import flatten_dict, nested_get, nested_set


PLIST_SCHEMA = {
  '1.0': [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">',
    '<plist version="1.0">',
    '<dict>',
    '</dict>',
    '</plist>'
  ]
}
"""Base Apple property list schemas.
@see https://www.apple.com/DTDs/PropertyList-1.0.dtd
"""

def parse_plist_types(stype: str,
                           value: str
                           ) -> Union[Tuple[str, any],  None]:
  """Parse property list types to Python types.

  Args:
    stype: Property list type (literal).
    value: Property list value.

  Returns:
    Tuple of (type, value) for the given type.
  """
  entry = None
  try:
    if   stype == 'array':    entry = []
    elif stype == 'data':     entry = ('data', b64decode(value.encode()).hex().upper())
    elif stype == 'date':     entry = (stype, datetime.fromisoformat(value.replace("Z", "+00:00")))
    elif stype == 'dict':     entry = {}
    elif stype == 'real':     entry = ('float', float(value))
    elif stype == 'integer':  entry = ('int', int(value))
    elif stype == 'string':   entry = ('string', value)
    elif stype == 'true':     entry = ('bool', True)
    elif stype == 'false':    entry = ('bool', False)
  except: pass # De-op
  return entry

def write_plist_types(value: Union[Tuple[str, any], any],
                           defaults: Union[Tuple[str, any], any]=('dict', None)
                           ) -> List[str]:
  """Parse Python types to property list entries.

  Args:
    value: Tuple of type (literal) and value.
    defaults: Fallback tuple of type (literal) and value.

  Returns:
    A list of property list entries.
  """

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
  # Parse entry value
  entry  = None
  if   stype == 'date':   svalue = str(svalue).replace(' ', 'T').replace('+00:00', 'Z')
  elif stype == 'string': pass
  # Handle alternate serialized types
  elif stype == 'float':  stype = 'real'
  elif stype == 'int':    stype = 'integer'
  # Handle alternate serialized values
  elif stype == 'data':   svalue = b64encode(bytes.fromhex(svalue)).decode()
  # Handle alternate entry schemas
  elif stype == 'bool':
    entry = [f'<{(stype := str(svalue).lower())}/>']
  else:
    entry = [f'<{stype}>', f'</{stype}>']
  # Default entry schema
  if entry is None:
    entry = [f'<{stype}>{svalue}</{stype}>']

  return entry

def parse_plist(lines: Union[List[str], TextIOWrapper],
                config: Optional[dict]=None
                ) -> dict:
  """Parses a property list into a Python dictionary.

  Args:
    lines: Property list (plist) lines.
    config: Dictionary to be populated.

  Returns:
    Dictionary populated from plist entries.
  """
  if config is None: config = dict()

  cursor = {
    'keys': [],
    'level': 0,
    'indent': 0,
    'skip': (def_flag := False),
    'prev_line': None
  }
  for line in lines:
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
      update_cursor(level, key, cursor)
    # Update dictionary values
    elif lnorm.startswith('<'):
      # Attempt single-line extraction of type and value
      stype = re.findall('<([a-z]+)/?>', lnorm, re.IGNORECASE)[0]
      value = re.findall('<[a-z]+>(.*)</[a-z]+>', lnorm, re.IGNORECASE)
      if len(value): value = value[0]

      # Extract and validate parent tree level
      tree = cursor['keys']
      while len(tree)-1 >= level / max(1, cursor['indent']):
        cursor['level'] -= cursor['indent']
        # Handle object arrays separately
        if cursor['prev_line'].lstrip().startswith(f'</{stype}>'):
          tree.pop(-1)
        # Handle dictionary keys separately
        else:
          tree.pop(-2)
      
      # Parse property list types to Python types
      # @see https://www.apple.com/DTDs/PropertyList-1.0.dtd
      entry = parse_plist_types(stype, value)
      if entry is None: continue

      # Handle object and array traversal
      ptree = tree[:-1] if stype != 'dict' else tree
      prev_value = nested_get(config, ptree)
      if isinstance(prev_value, dict) or prev_value is None:
        try:
          nested_set(config, tree, entry)
        except: pass #TODO: Handle pure array entries
      elif isinstance(prev_value, list):
        if stype == 'dict':
          # Always append dictionaries to arrays
          prev_value.append(entry)
          nested_set(config, ptree, prev_value)
        else:
          # Add new key to last dictionary in array
          *tree, key = tree
          prev_value[-1][key] = entry
          nested_set(config, tree, prev_value)
      # Update cursor position
      cursor['prev_line'] = line
    # Reached invalid line
    else: pass #TODO: Handle multi-line values
      # raise Exception(f'Invalid line at position {i}:\n\n{line}')

  return config

def write_plist(config: dict,
                lines: Optional[List[str]]=None,
                ) -> List[str]:
  """Writes a property list from a Python dictionary.

  Args:
    lines: Property list (plist) lines.
    config: Dictionary to be written.

  Returns:
    Property list (plist) populated from dictionary entries.
  """
  if lines is None: lines = PLIST_SCHEMA['1.0']

  def try_index(*args: Union[str, int]) -> int:
    try: return lines.index(*args)
    except: return -1
  cursor = { 'line': 0, 'indent': 2 }
  for (keys, value) in flatten_dict(config).items():
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
      elif (re_match := re.search(r'(.*)\[([0-9]+)\]', key)):
        key, idx = re_match.groups()
        tree[j] = key
        tree[j+1:j+1] = [int(idx)]
      
      # Search for key in current level
      key_ln = f'{padding}<key>{key}</key>'
      if (index := try_index(key_ln, head)) == -1:
        # Always append to end of dictionary
        if not lines[head].lstrip().startswith('</dict>'):
          while not lines[head-1].startswith(f'{padding}</'):
            head += 1
            if lines[head].startswith(f'{padding}<key>'): head += 1
            if lines[head].startswith(f'{padding[:-2]}</'): break
        # Append new entry
        defaults = ('dict' if not re_match else 'array', '' if is_root_key else None)
        lns = [f'{padding}{v}' for v in write_plist_types(value, defaults)]
        # Create a new key
        lines[head:head] = (entry := [key_ln, *lns])
        head += len(entry) - 1
      else:
        # Seek end of level
        if index >= head: head = index + 1
        for line in lines[head:]:
          if len(padding) < len(line[:-len(line.lstrip())]): head += 1
          else: break
        head += 1

  return lines


__all__ = [
  "PLIST_SCHEMA",
  "parse_plist_types",
  "write_plist_types",
  "parse_plist",
  "write_plist"
]
