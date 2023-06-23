## @file
# Parser for converting annotated YAML to a Python dictionary.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

import re
from shlex import split
from typing import Literal, Tuple

from parsers._lib import update_cursor
from parsers.dict import flatten_dict, nested_get, nested_set


def parse_serialized_types(stype: str,
                         value: str) -> Tuple[str, any] | None:
  """Parse YAML types to Python types.

  Args:
    stype: YAML type (literal).
    value: YAML value.

  Returns:
    Tuple of parsed type (literal) and value.
  """
  raise NotImplementedError() #TODO

def write_serialized_types(value: Tuple[str, any] | any,
                         schema=Literal['annotated', 'yaml']) -> Tuple[str, any]:
  """Parse Python types to YAML types.

  Args:
    value: Tuple of type (literal) and value.
    schema: Flag to control output schema.

  Returns:
    Tuple of parsed type (literal) and value.
  """

  # Unpack native types
  stype, svalue = type(value).__name__, value
  if isinstance(value, tuple): stype, svalue = value

  match schema:
    case 'annotated':
      # Parse native types
      match stype:
        case 'bool':      stype = 'Boolean'; svalue = str(svalue).lower()
        case 'data':      stype = 'Data   '; svalue = f'<{svalue}>'
        case 'dict':      stype = 'Dict   '; svalue = '(empty)'
        case 'float':     stype = 'Number '; svalue = str(float(svalue))
        case 'int':       stype = 'Number '; svalue = str(int(svalue))
        case 'list':      stype = 'Array  '; svalue = '(empty)'
        case 'string':    stype = 'String '; svalue = f'"{svalue}"'
        case _:
          stype = stype.rjust(len('       ')).capitalize()
          svalue = str(value)
    case 'yaml':
      # Parse native types
      match stype:
        case 'bool':    svalue = str(svalue).lower()
        case 'dict':    svalue = ''
        case 'list':    svalue = ''
        case 'string':  svalue = f'"{svalue}"'
        case _:         svalue = str(svalue)
      # Escape control and reserved characters
      # @see https://symfony.com/doc/current/reference/formats/yaml.html
      reserve_chars = [':',     '{',    '}',    '[',    ']',    ',',    '&',
                       '*',     '#',    '?',    '|',    '-',    '<',    '>',
                       '=',     '!',    '%',    '@',    '`']
      control_chars = ['\0',    '\x01', '\x02', '\x03', '\x04', '\x05', '\x06',
                       '\a',    '\b',   '\t',   '\n',   '\v',   '\f',   '\r',
                       '\x0e',  '\x0f', '\x10', '\x11', '\x12', '\x13', '\x14',
                       '\x15',  '\x16', '\x17', '\x18', '\x19', '\x1a', r'\e',
                       '\x1c',  '\x1d', '\x1e', '\x1f', r'\N',  r'\_',  r'\L',
                       r'\P']
      if any([c for c in control_chars if c in svalue]):
        svalue = f'"{svalue}"'
      elif any([c for c in reserve_chars if c in svalue]):
        svalue = f'\'{svalue}\''
  
  return stype, svalue

def parse_yaml(lines: list[str],
              config: dict=dict(),
              flags: list[str]=[]):
  """Parses YAML (optionally type annotated) into a Python dictionary.

  Args:
    lines: YAML lines.
    config: Dictionary to be populated.
    flags: List of preprocessor flags.

  Returns:
    Dictionary populated from YAML entries.
  """
  cursor = { 'keys': [], 'level': 0, 'indent': 0, 'skip': (def_flag := False) }
  for i,line in enumerate(lines):
    # Skip empty lines
    if len(lnorm := line.lstrip().rstrip()) == 0:
      continue
    # Check if first non-whitespace character is a comment
    if lnorm.startswith('#'):
      continue

    # Extract tokens from line
    tokens = [p for p in split(lnorm) if (p != '|' and p != '-')]
    key = tokens[0][:-1] if (num_tokens := len(tokens)) else None

    # Handle preprocessor macros
    if (macro := tokens[0]).startswith('@'):
      flag = tokens[1] if num_tokens == 2 else def_flag
      match macro:
        case '@ifdef': cursor['skip'] = flag in flags
        case '@endif': cursor['skip'] = def_flag
      continue
    elif cursor['skip']: continue
    
    level = len(line[:-len(lnorm)])
    # Update cursor position
    if num_tokens == 1 and tokens[0].endswith(':'):
      update_cursor(level, key, cursor)
    # Update dictionary values
    elif num_tokens >= 1:
      # Extract schema and entry value
      schema = 'plist' if num_tokens >= 3 else 'yaml'
      entry = None
      match schema:
        case 'plist': entry = (tokens[1], ' '.join(tokens[2:]))
        case 'yaml':  entry = ' '.join(tokens[1:])

      # TODO: Parse YAML types to Python types
      # entry = parseSerializedTypes(...)

      # Extract and validate parent tree level
      tree = cursor['keys']
      while len(tree) >= level / max(1, cursor['indent']): tree.pop(-1)
      prev_value = nested_get(config, tree)
      
      # Handle initial array values
      if lnorm.startswith('-'):
        obj = { key: entry } if num_tokens > 1 else key
        if isinstance(prev_value, list):
          prev_value.append(obj)
          nested_set(config, tree, prev_value)
        else:
          nested_set(config, tree, [obj])
      else:
        # Handle object and array traversal
        match prev_value:
          case dict() | None:
            nested_set(config, [*tree, key], entry)
          case list():
            match prev_value[-1]:
              # Add new key to last dictionary in array
              case dict():  prev_value[-1][key] = entry
              # Always append dictionaries to arrays
              case _:       prev_value.append(entry)
            nested_set(config, tree, prev_value)
    # Reached invalid line
    else: raise Exception(f'Invalid line at position {i}:\n\n{line}')
  
  return config

def write_yaml(lines: list[str]=[],
              config: dict=dict(),
              schema: Literal['annotated', 'yaml']='yaml'):
  """Writes a Python dictionary to YAML.
  
  Args:
    lines: YAML lines.
    config: Dictionary to be written.
    schema: Flag to control output schema.

  Returns:
    YAML lines populated from dictionary entries.
  """
  cursor = { 'keys': [], 'indent': 2 }
  flat_dict = flatten_dict(config)

  # Pre-process and prettify tree indentations
  trees = []; max_tree_len = 0
  for keys in flat_dict.keys():
    # Seek or create head index for current tree level
    for j, key in enumerate(tree := str(keys).split('.')):
      # Avoid parsing literal array indices
      if isinstance(tree[j], int): continue
      # Insert array indices as additional keys
      elif (re_match := re.search('(.*)\[([0-9]+)\]', key)):
        key, idx = re_match.groups()
        tree[j] = key
        tree[j+1:j+1] = [int(idx)]
      
      # Update trees entries
      if j == len(tree)-1: trees.append(tree)
      else: continue

      # Update max tree length
      if schema == 'annotated':
        tree_len = cursor['indent']*j + len(f"{key}:")
        # Update max tree length
        if max_tree_len < tree_len: max_tree_len = tree_len
        
  # Write entries to lines
  for (tree, value) in zip(trees, flat_dict.values()):
    # Seek or create head index for current tree level
    for j, key in enumerate(tree):
      # Avoid inserting literal array indices
      if isinstance(tree[j], int):
        cursor['keys'].append(key)
        continue
      # Avoid inserting duplicate keys
      elif tree[:j+1] == cursor['keys'][:j+1]:
        continue

      # Add new key entry to last dict
      padding = (" "*cursor['indent'])*j
      entry = None
      if (is_root_key := (j == len(tree)-1)):
        # Handle indentation for first array item
        if isinstance(tree[j-1], int) and tree[:j] != cursor['keys'][:j]:
          padding = f'{padding[:-2]}- '
        # Append value to entry
        stype, svalue = write_serialized_types(value, schema)
        match schema:
          case 'annotated':
            indent = max_tree_len - (cursor['indent']*j + len(f"{key}:"))
            entry = f'{padding}{key}:{" ".rjust(indent + 1)}{stype} | {svalue}'
          case 'yaml':
            entry = f'{padding}{key}: {svalue}'.rstrip()
      # Add new dict
      else: entry = f'{padding}{key}:'
      lines.append(entry)

      # Update cursor position
      if is_root_key: cursor['keys'] = tree[:j+1]
      
  return lines
