## @file
# Parser for converting annotated YAML to a Python dictionary.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

from shlex import split

from parsers._lib import _updateCursor
from parsers.dict import nestedGet, nestedSet


def parseYAML(lines: list[str],
              config: dict=dict(),
              flags: list[str]=[]):
  """Parses annotated YAML into a Python dictionary.

  Args:
    lines: Annotated YAML lines.
    config: Dictionary to be populated.
    flags: List of preprocessor flags.

  Returns:
    Dictionary populated from annotated YAML entries.
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
      _updateCursor(level, key, cursor)
    # Update dictionary values
    elif num_tokens >= 1:
      # Extract schema and entry value
      schema = 'plist' if num_tokens >= 3 else 'yaml'
      entry = None
      match schema:
        case 'plist': entry = (tokens[1], ' '.join(tokens[2:]))
        case 'yaml':  entry = ' '.join(tokens[1:])

      # Extract and validate parent tree level
      tree = cursor['keys']
      while len(tree) >= level / max(1, cursor['indent']): tree.pop(-1)
      prev_value = nestedGet(config, tree)
      
      # Handle initial array values
      if lnorm.startswith('-'):
        obj = { key: entry } if num_tokens > 1 else key
        if isinstance(prev_value, list):
          prev_value.append(obj)
          nestedSet(config, tree, prev_value)
        else:
          nestedSet(config, tree, [obj])
      else:
        # Handle object and array traversal
        match prev_value:
          case dict() | None:
            nestedSet(config, [*tree, key], entry)
          case list():
            match prev_value[-1]:
              # Add new key to last dictionary in array
              case dict():  prev_value[-1][key] = entry
              # Always append dictionaries to arrays
              case _:       prev_value.append(entry)
            nestedSet(config, tree, prev_value)
    # Reached invalid line
    else: raise Exception(f'Invalid line at position {i}:\n\n{line}')
  
  return config
