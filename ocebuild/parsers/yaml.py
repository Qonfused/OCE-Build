## @file
# Parser for converting annotated YAML to a Python dictionary.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

import re
from shlex import split
from typing import List, Literal, Optional, Tuple, Union

from ocebuild.parsers._lib import update_cursor
from ocebuild.parsers.dict import flatten_dict, nested_get, nested_set


def parse_serialized_types(stype: str,
                           value: str
                           ) -> Union[Tuple[str, any], None]:
  """Parse YAML types to Python types.

  Args:
    stype: YAML type (literal).
    value: YAML value.

  Returns:
    Tuple of parsed type (literal) and value.
  """
  raise NotImplementedError() #TODO

def write_serialized_types(value: Union[Tuple[str, any], any],
                           schema: Literal['annotated', 'yaml']='yaml'
                           ) -> Tuple[str, any]:
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

  if schema == 'annotated':
    print('..', stype, svalue)
    # Parse native types
    if   stype == 'date':     stype = 'Date   '; svalue = str(svalue).replace(' ', 'T').replace('+00:00', 'Z')
    elif stype == 'bool':     stype = 'Boolean'; svalue = str(svalue).lower()
    elif stype == 'data':     stype = 'Data   '; svalue = f'<{svalue}>'
    elif stype == 'dict':     stype = 'Dict   '; svalue = '(empty)'
    elif stype == 'float':    stype = 'Number '; svalue = str(float(svalue))
    elif stype == 'int':      stype = 'Number '; svalue = str(int(svalue))
    elif stype == 'list':     stype = 'Array  '; svalue = '(empty)'
    elif stype == 'string':   stype = 'String '; svalue = f'"{svalue}"'
    else:
      stype =         stype.rjust(len('       ')).capitalize()
      svalue = str(value if not isinstance(value, tuple) else value[1])
    # print(stype, svalue)
  elif schema == 'yaml':
    # Parse native types
    if   stype == 'bool':     svalue = str(svalue).lower()
    elif stype == 'dict':     svalue = ''
    elif stype == 'list':     svalue = ''
    elif stype == 'string':   svalue = f'"{svalue}"'
    else:                     svalue = str(svalue)
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

def parse_yaml(lines: List[str],
               config: Optional[dict]=None,
               flags: Optional[List[str]]=None,
               frontmatter: bool=False
               ) -> Union[dict, Tuple[dict, dict]]:
  """Parses YAML (optionally type annotated) into a Python dictionary.

  Args:
    lines: YAML lines.
    config: Dictionary to be populated.
    flags: List of preprocessor flags.
    frontmatter: 

  Returns:
    Dictionary populated from YAML entries.
  """
  if config is None: config = dict()
  if flags is None: flags = []
  frontmatter_dict: Optional[dict]=dict()
  
  i = 0
  cursor = {
    'keys': [],
    'level': 0,
    'indent': 0,
    'skip': (def_flag := False),
    'upshift': False,
    'is_frontmatter': False
  }
  for _line in lines:
    i += 1; line = _line.rstrip()
    # Skip empty lines
    if len(lnorm := line.lstrip()) == 0:
      continue
    # Check if first non-whitespace character is a comment
    if lnorm.startswith('#'):
      continue
    # Check if crossing frontmatter
    if lnorm.startswith('---'):
      cursor['is_frontmatter'] = not cursor['is_frontmatter']
      continue

    # Extract tokens from line
    tokens = [p for p in split(lnorm) if (p != '|' and p != '-')]
    key = tokens[0][:-1] if (num_tokens := len(tokens)) else None
    def get_schema(schema: Literal['plist', 'yaml']) -> Union[Tuple[str, str], str]:
      if schema == 'plist':
        return (tokens[1], ' '.join(tokens[2:]))
      elif schema == 'yaml':
        return ' '.join(tokens[1:])
    
    # Handle parsing frontmatter variables
    if cursor['is_frontmatter']:
      frontmatter_dict[key] = get_schema('yaml')
      continue
    # def get_frontmatter():
    #   """Replaces variables with frontmatter values"""

    # Handle preprocessor macros
    if (macro := tokens[0][:-1]).startswith('@'):
      flag = tokens[1] if num_tokens == 2 else def_flag
      # Check if flag exists
      if   macro == '@ifdef':
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
        cursor['skip'] = def_flag
      continue
    # Skip through macro checking scope
    elif cursor['skip']: continue
    
    # Handle non-dict yaml arrays
    if lnorm.startswith('- ') and ': ' not in lnorm:
      # Extract correct value from tokens
      key = tokens[0]
      cursor['upshift'] = True
    # Fix subsequent non-array entries
    elif cursor['upshift']:
      # Treat cursor as if it's in the same level as normal dict keys
      cursor['keys'] = cursor['keys'][:-1]
      cursor['level'] -= cursor['indent']
      cursor['upshift'] = False
    
    # Update cursor position
    level = len(line[:-len(lnorm)])
    if num_tokens == 1 and tokens[0].endswith(':'):
      update_cursor(level, key, cursor, upshift=1)
    # Update dictionary values
    elif num_tokens >= 1:
      # Extract schema and entry value
      schema = 'plist' if num_tokens >= 3 else 'yaml'
      entry = get_schema(schema)

      # TODO: Parse YAML types to Python types
      # entry = parseSerializedTypes(...)

      # Extract and validate parent tree level
      tree = cursor['keys']
      while len(tree) > level / max(1, cursor['indent']):
        tree.pop(-1)
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
        if isinstance(prev_value, dict) or prev_value is None:
          nested_set(config, [*tree, key], entry)
        elif isinstance(prev_value, list):
          # Add new key to last dictionary in array
          if isinstance(prev_value[-1], dict):
            prev_value[-1][key] = entry
          # Always append dictionaries to arrays
          else:
            prev_value.append(entry)
          # Update array
          nested_set(config, tree, prev_value)
    # Reached invalid line
    else: raise Exception(f'Invalid line at position {i}:\n\n{line}')
  
  if frontmatter: return config, frontmatter_dict
  return config

def write_yaml(config: dict,
               lines: Optional[List[str]]=None,
               schema: Literal['annotated', 'yaml']='yaml'
               ) -> List[str]:
  """Writes a Python dictionary to YAML.
  
  Args:
    lines: YAML lines.
    config: Dictionary to be written.
    schema: Flag to control output schema.

  Returns:
    YAML lines populated from dictionary entries.
  """
  if lines is None: lines = []

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
      elif (re_match := re.search(r'(.*)\[([0-9]+)\]', key)):
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
        if schema == 'annotated':
          indent = max_tree_len - (cursor['indent']*j + len(f"{key}:"))
          entry = f'{padding}{key}:{" ".rjust(indent + 1)}{stype} | {svalue}'
        elif schema == 'yaml':
          entry = f'{padding}{key}: {svalue}'.rstrip()
      # Add new dict
      else: entry = f'{padding}{key}:'
      lines.append(entry)

      # Update cursor position
      if is_root_key: cursor['keys'] = tree[:j+1]
      
  return lines
