## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Methods for retrieving and handling Sample.plist schemas."""

from io import TextIOWrapper

from typing import List, Set, Tuple, Union

from .dict import nested_get, nested_set
from .regex import re_search
from .yaml import parse_yaml_types


################################################################################
#                               LaTeX Parsing Macros                           #
################################################################################

def _extract_command(line: str) -> Union[str, None]:
  """Extracts a LaTeX command from a line."""

  if line[:1] == '\\' and (command_match := line.split('{', 1)[0])[1:]:
    # Handle match on labels, etc
    if command_match.count('\\') > 1:
      return command_match.split(maxsplit=1)[0]
    # Default to prefix match
    return command_match
  else:
    # No match
    return None

def _extract_key(command: str, string: str, sol='^') -> Union[str, None]:
  """Extracts a key value from a line."""
  return re_search(f'{sol}\{command}\{{(.*?)\}}', string, group=1)

def _extract_value(command: str,
                   string: str,
                   key: str,
                   eol='\\\\\\\\'
                   ) -> Union[str, None]:
  """Extracts a key value from a line."""
  ln = re_search(f'\{command}\{{{key}\}}:\s?(.*){eol}$', string, group=1)
  if not ln or not eol: return ln
  return _extract_key(command='\.*?', string=ln.strip(), sol='^') or ln

def _parse_attributes(line: str, key: str) -> str:
  skey = key.replace('\\', '\\\\')
  if attr := re_search(f'\{{{skey}\}},?\s?(.*?)\\\\\\\\$', line, group=1):
    key += f", {attr}"
  return key

def _normalize_lines(entry: str) -> str:
  """Normalizes indentation errors."""
  lines = []
  for i, e in enumerate(entry.split('\n\n\n\n')):
    lines.append(e.replace('\n\n  ', ' ' if i else '\n').strip())

  return "\n\n".join(lines)

################################################################################
#                              Entry Parsing Macros                            #
################################################################################

def _reset_key_entry(cursor: dict):
  """Resets the cursor's key attributes."""
  cursor['key'] = None
  cursor['type'] = None
  cursor['value'] = None
  cursor['entry'] = None

def _parse_key_entry(cursor: dict, schema: dict, sample: dict):
  """Add value to the schema if all required attributes are present"""

  tree = cursor['tree'].copy()
  queue = [tree]

  # Attempt to fix values inconsistent with the sample plist
  if not nested_get(sample, tree):
    # 'Entry Properties' has an inconsistent name
    if tree == ['Misc', 'Entry']:
      tree[-1] = 'Entries'
      # These properties are also applicable to `Misc.Tools`
      queue += [('Misc', 'Tools')]
    # 'Memory Device Properties' has an inconsistent name
    if tree == ['PlatformInfo', 'Memory', 'Device']:
      tree[-1] = 'Devices'

  # Add entries to the schema
  for tree_ in queue: _add_schema_entry(tree_, cursor, schema)

def _parse_exclusion_rules(cursor: dict) -> Tuple[Set[str], Set[str]]:
  """Parses exclusion rules from an entry description."""

  # Set default allowlist based on parent key
  valid = set(cursor['tree'][-1:])
  invalid = set()

  if entry := cursor['entry']:
    # Parse description for exclusion/inclusion rules
    valid_pattern = r'\\emph\{Note\}: This option is only valid for \\texttt\{(.*?)\}'
    if valid_match := re_search(valid_pattern, entry, group=1):
      valid = set((valid_match,))
    invalid_pattern = valid_pattern + r' and cannot be specified for \\texttt\{(.*?)\}'
    if invalid_match := re_search(invalid_pattern, entry, group=2):
      invalid = set((invalid_match,))

  return valid, invalid

def _parse_failsafe(stype: str,
                    svalue: str
                    ) -> Union[str, int, float, dict, list]:
  """Parses a failsafe value."""

  # Remove leading and trailing whitespace
  atype = stype\
    .strip() \
    .replace('plist\\ ', '') \
    .split(',')[0] \
    .capitalize()

  if atype in ('Integer', 'Real'):
    atype = 'Number'
    # Handle typecasting for hexadecimal values
    if svalue[:2] == '0x':
      svalue = str(int(svalue, 16))
  elif atype in ('Data', 'Multidata'):
    atype = 'Data'
    if svalue[:2] == '0x':
      svalue = svalue[2:]
    # Handle filling size-specified data values
    if   size := re_search(', (\d+) bits?', stype, group=1):
      svalue = '0' * 1 * int(size)
    elif size := re_search(', (\d+) bytes?', stype, group=1):
      svalue = '0' * 2 * int(size)
  elif atype in ('Dictionary'):
    atype = 'Dict'

  if svalue.lower().split(maxsplit=1)[0] in ('empty',):
    svalue = ''

  # Ensure value is serializable as an annotated YAML type
  value = parse_yaml_types(atype, svalue, schema='annotated')

  return value

################################################################################
#                              Schema Parsing Methods                          #
################################################################################

def _add_schema_entry(tree: list, cursor: dict, schema: dict):
  """Parse and add failsafe values"""

  # Ensure that the parent entry is a valid target
  valid, invalid = _parse_exclusion_rules(cursor)
  pkey = tree[-1]
  if pkey not in valid and pkey in invalid: return

  # Parse failsafe value
  key = cursor['key']
  stype = cursor['type']
  svalue = cursor['value'] or 'Empty'
  entry = _parse_failsafe(stype, svalue)

  # Ensure that the parent entry exists in the schema
  parent_entry = nested_get(schema, tree, default={})
  if not parent_entry: nested_set(schema, tree, {})

  if   isinstance(parent_entry, dict):
    nested_set(schema, (*tree, key), entry)
  elif isinstance(parent_entry, list):
    # Only one dict entry is allowed per array
    if not parent_entry: parent_entry = [{}]
    parent_entry[0][key] = entry
    nested_set(schema, tree, parent_entry)

def parse_schema(file: Union[List[str], TextIOWrapper],
                 sample_plist: dict
                 ) -> dict:
  """Gets the Sample.plist schema from a Configuration.tex file.

  The Sample.plist schema is parsed from the Configuration.tex file, which is
  the source LaTeX file for the OpenCore documentation. These schema values
  match the declared failsafe values used as fallbacks in the OpenCore config
  file. Extracted schema values are then converted to a plist-compatible format
  and then coerced into native Python types.

  Args:
    file: The Configuration.tex file to parse.
    sample_plist: The sample plist to use for comparison.

  Returns:
    A dictionary representing failsafe values for the Sample.plist schema.
  """

  # Parse the configuration schema against the sample plist
  cursor = { 'tree': [], 'key': None, 'type': None, 'value': None, 'entry': '' }
  schema = {}
  for line in file:
    # Normalize line
    lnorm = str(line.lstrip()).strip()
    # Skip comments
    if lnorm[:1] == '%': continue

    # Use root-level commands as boundaries for key entries
    if (line[:1] == '\\' or lnorm.startswith('\item')) and cursor['key']:
      if (entry := cursor['entry']) and cursor['type']:
        # Normalize entry to fix formatting inconsistencies
        cursor['entry'] = _normalize_lines(entry)
        # Add key entry to schema
        _parse_key_entry(cursor, schema, sample_plist)
      # Reset all attributes
      _reset_key_entry(cursor)
    # If set, continue storing the current LaTeX entry
    elif cursor['entry']:
      cursor['entry'] += f"\n{line}"

    # Parse LaTeX commands
    if command := _extract_command(lnorm):
      # Parse section/subsection commands
      if command in ('\section', '\subsection', '\subsubsection'):
        name: str = re_search(f'\\{command}\{{(.*?)\}}', lnorm, group=1)
        # Is a section
        if command == '\section':
          entry = [name] if name in sample_plist.keys() else []
          cursor['tree'] = entry
        # Is a subsection
        else:
          key = re_search(r'([a-zA-Z0-9]+)\s?Properties', name, group=1)
          if command == '\subsection':
            entry = [key] if key else []
            cursor['tree'][1:] = entry
          elif command == '\subsubsection':
            entry = key.split(maxsplit=1)[:1] if key else []
            cursor['tree'][2:] = entry
      # Parse property fields for keys
      elif cursor['tree'] and command in ('\\texttt', '\\textbf'):
        if command == '\\texttt':
          # Is a key name
          if key := _extract_key(command, lnorm, sol=''):
            if not cursor['key']:
              cursor['key'] = key
              cursor['entry'] = line
        elif command == '\\textbf':
          # Is a key type
          if stype := _extract_value(command, lnorm, key='Type'):
            # Append additional attributes outside of the encapsulated value
            cursor['type'] = _parse_attributes(lnorm, stype)
          # Is a key value
          elif svalue := _extract_value(command, lnorm, key='Failsafe'):
            cursor['value'] = svalue

  return schema


__all__ = [
  # Functions (1)
  "parse_schema"
]
