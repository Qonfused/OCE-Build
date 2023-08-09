## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Parser for converting annotated YAML to a Python dictionary."""

#pylint: disable=cell-var-from-loop

from datetime import datetime
from shlex import split

from typing import List, Literal, Optional, Tuple, Union

from ._lib import _append_tags, _apply_macro, update_cursor
from .dict import flatten_dict, nested_get, nested_set
from .regex import re_search
from .types import decode_data, encode_data


def parse_yaml_types(stype: str,
                     value: str,
                     schema: Literal['annotated', 'yaml']='yaml'
                     ) -> Union[Tuple[str, any], None]:
  """Parse YAML types to Python types.

  Args:
    stype: YAML type (literal).
    value: YAML value.
    schema: Flag to control input schema.

  Returns:
    Tuple of parsed type (literal) and value.
  """
  svalue = None
  if schema == 'annotated':
    # Parse annotated types
    if   stype == 'Date':
      svalue = datetime.fromisoformat(value.replace("Z", "+00:00"))
    elif stype == 'Boolean':
      svalue = bool(value.lower() == 'true')
    elif stype == 'Data':
      stype = 'data'
      svalue = encode_data(value)
    elif stype == 'Dict':
      svalue = {}
    elif stype == 'Number':
      if '.' in value:
        svalue = float(value)
      else:
        svalue = int(value)
    elif stype == 'Array':
      svalue = []
    elif stype == 'String':
      svalue = value
    # Handle generic or string types
    if isinstance(svalue, str) and svalue[:1] in ('"', "'"):
      svalue = svalue[1:-1]
    return svalue
  elif schema == 'yaml':
    raise NotImplementedError() #TODO

def write_yaml_types(value: Union[Tuple[str, any], any],
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

  def _format_data(data, pad=8):
    """Formats data into hex strings"""
    string = decode_data(data, enc='hex')
    hex_fmt = ' '.join(string[i:i+pad] for i in range(0,len(string), pad))
    return f"<{ hex_fmt }>"

  if schema == 'annotated':
    # Parse native types
    if   stype == 'date':
      stype = 'Date   '; svalue = str(svalue).replace(' ', 'T').replace('+00:00', 'Z')
    elif stype in ('bool', 'boolean'):
      stype = 'Boolean'; svalue = str(svalue).lower()
    elif stype in ('bytes', 'data'):
      stype = 'Data   '; svalue = _format_data(svalue)
    elif stype in ('dict', 'dictionary'):
      stype = 'Dict   '; svalue = '(empty)'
    elif stype == 'float':
      stype = 'Number '; svalue = str(float(svalue))
    elif stype in ('int', 'integer'):
      stype = 'Number '; svalue = str(int(svalue))
    elif stype in ('list', 'array'):
      stype = 'Array  '; svalue = '(empty)'
    elif stype in ('str', 'string'):
      stype = 'String '; svalue = f'"{svalue}"'
    else:
      max_size = len('Boolean')
      stype = stype.rjust(max_size).capitalize()
      svalue = str(value if not isinstance(value, tuple) else value[1])
  elif schema == 'yaml':
    # Parse native types
    if   stype in ('bool', 'boolean'):
      svalue = str(svalue).lower()
    elif stype in ('dict', 'object'):
      svalue = ''
    elif stype in ('list', 'array'):
      svalue = ''
    elif stype in ('str', 'string'):
      svalue = f'"{svalue}"'
    else:
      svalue = str(svalue)

    # Remove existing quotes from strings
    for quote in ('"', "'"):
      if svalue.startswith(quote) and svalue.endswith(quote):
        svalue = svalue[1:-1]

    # Escape control and reserved characters
    # @see https://symfony.com/doc/current/reference/formats/yaml.html
    reserve_chars = (':',     '{',    '}',    '[',    ']',    ',',    '&',
                     '*',     '#',    '?',    '|',    '-',    '<',    '>',
                     '=',     '!',    '%',    '@',    '`')
    control_chars = ('\0',    '\x01', '\x02', '\x03', '\x04', '\x05', '\x06',
                     '\a',    '\b',   '\t',   '\n',   '\v',   '\f',   '\r',
                     '\x0e',  '\x0f', '\x10', '\x11', '\x12', '\x13', '\x14',
                     '\x15',  '\x16', '\x17', '\x18', '\x19', '\x1a', r'\e',
                     '\x1c',  '\x1d', '\x1e', '\x1f', r'\N',  r'\_',  r'\L',
                     r'\P')
    if any(c for c in control_chars if c in svalue):
      svalue = f'"{svalue}"'
    elif any(c for c in reserve_chars if c in svalue):
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
    frontmatter: Flag to control frontmatter parsing.

  Raises:
    ValueError: If YAML parser reaches an invalid line.

  Returns:
    Dictionary populated from YAML entries.
  """
  if config is None: config = {}
  if flags is None: flags = []
  frontmatter_dict = { 'variables': {}, 'tags': [] }

  i = 0
  cursor = {
    'keys': [],
    'level': 0,
    'indent': 0,
    'skip': False,
    'upshift': False,
    'is_frontmatter': False,
    'has_tag': None,
    'tag_tree': None
  }
  for line_ in lines:
    i += 1; line = line_.rstrip()
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
    tokens = [p for p in split(lnorm) if p not in ('|', '-')]
    key = tokens[0][:-1] if (num_tokens := len(tokens)) else None
    def get_schema(schema: Literal['annotated', 'yaml']
                   ) -> Union[Tuple[str, str], str]:
      if schema == 'annotated':
        return parse_yaml_types(tokens[1], ' '.join(tokens[2:]), schema)
      elif schema == 'yaml':
        return ' '.join(tokens[1:])

    # Handle parsing frontmatter variables
    if cursor['is_frontmatter']:
      value = get_schema('yaml')
      nested_set(frontmatter_dict, ['variables', key], value)
      # Add OpenCore build type as global flag
      if key in ('build', 'target'): flags += [value]
      continue
    # Handle preprocessor macros
    elif (macro := tokens[0]).startswith('@'):
      # Fix comma-separated macro flags
      if macro[-1] == ',':
        for token in tokens[1:]: macro += token
      _apply_macro(macro, flags, cursor, frontmatter_dict)
      continue
    # Skip through macro checking scope
    elif cursor['skip']:
      continue

    #TODO: Handle parsing frontmatter variables
    # def get_frontmatter():
    #   """Replaces variables with frontmatter values"""

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
      cursor['tag_tree'] = cursor['keys']
    # Update dictionary values
    elif num_tokens >= 1:
      # Extract schema and entry value
      schema = 'annotated' if num_tokens >= 3 else 'yaml'
      entry = get_schema(schema)

      # Extract and validate parent tree level
      tree = cursor['keys']
      while len(tree) > level / max(1, cursor['indent']):
        tree.pop(-1)
        cursor['level'] -= cursor['indent']
      prev_value = nested_get(config, tree)

      # Handle inline objects or arrays
      if len(tokens) >= 2:
        if len(tokens) > 3 and tokens[1] in ('{', '['):
          tokens = [tokens[0], ' '.join(tokens[1:])]
          entry = tokens[1]
        elif tokens[1][0] == '{' and tokens[1][-1] == '}':
          entry = tokens[1]

      # Handle initial array values
      if lnorm.startswith('-'):
        obj = { key: entry } if num_tokens > 1 else key
        if isinstance(prev_value, list):
          prev_value.append(obj)
          nested_set(config, tree, prev_value)
          cursor['tag_tree'] = tree + [len(prev_value) - 1]
        else:
          nested_set(config, tree, [obj])
          cursor['tag_tree'] = tree + [0]
      else:
        cursor['tag_tree'] = tree + [key]
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
    else:
      raise ValueError(f'Invalid line at position {i}:\n\n{line}')

    _append_tags(cursor, frontmatter_dict)

  if frontmatter:
    frontmatter_dict['flags'] = flags
    return config, frontmatter_dict
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
  for keys in flat_dict:
    # Seek or create head index for current tree level
    for j, key in enumerate(tree := str(keys).split('.')):
      # Avoid parsing literal array indices
      if isinstance(tree[j], int): continue
      # Insert array indices as additional keys
      elif (re_match := re_search(r'(.*)\[([0-9]+)\]', key, group=None)):
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
        max_tree_len = max(max_tree_len, tree_len)

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
      if is_root_key := j == len(tree)-1:
        # Handle indentation for first array item
        if isinstance(tree[j-1], int) and tree[:j] != cursor['keys'][:j]:
          padding = f'{padding[:-2]}- '
        # Append value to entry
        stype, svalue = write_yaml_types(value, schema)
        if schema == 'annotated':
          as_literal = False
          indent = max_tree_len - (cursor['indent']*j + len(f"{key}:"))
          # Add indentation for comments
          if key.startswith('#'):
            comment_key = key[1:].split()[0].lower()
            if comment_key in ('warning', 'comment'):
              as_literal = True
            else:
              indent += 2 if key[:2] == '# ' else 1
          # Format indentation-aligned entries
          if as_literal:
            entry = f'{padding}{key}: {value}'
          else:
            entry = f'{padding}{key}:{" ".rjust(indent + 1)}{stype} | {svalue}'
        elif schema == 'yaml':
          entry = f'{padding}{key}: {svalue}'.rstrip()
      # Add new dict
      else:
        if key.startswith('#'):
          key = f"'{key}'"
        entry = f'{padding}{key}:'
      lines.append(entry)

      # Update cursor position
      if is_root_key: cursor['keys'] = tree[:j+1]

  return lines


__all__ = [
  # Functions (4)
  "parse_yaml_types",
  "write_yaml_types",
  "parse_yaml",
  "write_yaml"
]
