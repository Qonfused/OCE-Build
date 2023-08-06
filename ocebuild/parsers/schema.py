## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Methods for retrieving and handling Sample.plist schemas."""

from io import TextIOWrapper

from typing import List, Optional, Set, Tuple, Union

from .dict import nested_get, nested_set
from .regex import re_search
from .yaml import parse_yaml_types


################################################################################
#                               LaTeX Parsing Macros                           #
################################################################################

def _extract_command(line: str) -> Union[str, None]:
  """Extracts a LaTeX command from a line.

  Examples:
    >>> _extract_command('\\section{foo}')
    '\\\\section'
    >>> _extract_command('\\\\texttt{foo} \\label{bar}')
    '\\\\texttt'
    >>> _extract_command('% \\\\foo')
    None
  """

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
  """Extracts a key name from a line.

  Args:
    command: The LaTeX command to match.
    string: The intput string to match against.
    sol: The start of line character to match against. Defaults to '^'.

  Returns:
    The matched key name or None if no match was found.

  Examples:
    >>> _extract_key('\\\\texttt', '\\\\texttt{foo}')
    'foo'
    >>> _extract_key('\\\\texttt', '\\\\texttt{foo} \\label{bar}')
    'foo'
    >>> _extract_key('\\\\texttt', '\\\\texttt{foo} \\texttt{bar}', sol='')
    'bar'
    >>> _extract_key('\\\\label', '\\\\texttt{foo}')
    None
  """
  return re_search(f'{sol}\\{command}\\{{(.*?)\\}}', string, group=1)

def _extract_value(command: str,
                   string: str,
                   key: str,
                   eol='\\\\\\\\'
                   ) -> Union[str, None]:
  """Extracts a key value from a line.

  Args:
    command: The LaTeX command to match.
    string: The intput string to match against.
    key: The key name to match against.
    eol: The end of line character to match against. Defaults to '\\\\\\\\'.

  Returns:
    The matched key value or None if no match was found.

  Examples:
    >>> _extract_value('\\\\textbf', '\\\\textbf{Type}: foo\\\\\\\\', 'Type')
    'foo'
    >>> _extract_value('\\\\textbf', '\\\\textbf{Type}: foo \\\\texttt{bar}\\\\\\\\', 'Type')
    'foo \\\\texttt{bar}'
  """
  ln = re_search(f'\\{command}\\{{{key}\\}}:\\s?(.*){eol}$', string, group=1)
  if not ln or not eol: return ln
  return _extract_key(command='\\.*?', string=ln.strip(), sol='^') or ln

def _parse_attributes(line: str, key: str) -> str:
  """Parses additional attributes from a line.

  Args:
    line: The line to parse.
    key: The key to append attributes to.

  Returns:
    The key with appended attributes.

  Example:
    >>> _parse_attributes('\\\\textbf{Type}: \\\\texttt{foo}, bar\\\\\\\\', 'Type')
    'foo, bar'
  """
  skey = key.replace('\\', '\\\\')
  if attr := re_search(f'\\{{{skey}\\}},?\\s?(.*?)\\\\\\\\$', line, group=1):
    key += f", {attr}"
  return key

def _normalize_lines(entry: str) -> str:
  """Normalizes indentation errors."""
  lines = []
  for i, e in enumerate(entry.split('\n\n\n\n')):
    line_fmt = e \
      .replace('\n\n  ', ' ' if i else '\n') \
      .replace('\\newline ', '\n') \
      .strip()
    # Handle inconsistent indentation in the primary entry
    line_fmt = "".join(f"\n{l}" if l[:1] == '\\' and (not i or '}:' in l) \
                            else f" {l}" \
                        for i, l in enumerate(line_fmt.split('\n')))

    lines.append(line_fmt.strip())

  # Handle exceptions for specific commands
  line_fmt = "\n\n".join(lines).replace('  ', '') \
    .replace(cmd := '\\begin{itemize}', f'\n{cmd}') \
    .replace(f'\n\n{cmd}', f'\n{cmd}') \
    .replace(cmd := '\\tightlist',      f'\n  {cmd}') \
    .replace(cmd := '\\item',           f'\n  {cmd}') \
    .replace(cmd := '\\end{itemize}',   f'\n{cmd}')

  return line_fmt

################################################################################
#                              Entry Parsing Macros                            #
################################################################################

def _reset_key_entry(cursor: dict):
  """Resets the cursor's key attributes."""
  cursor['key'] = None
  cursor['type'] = None
  cursor['value'] = None
  cursor['entry'] = None

def _parse_key_entry(cursor: dict,
                     schema: dict,
                     sample: dict,
                     /,
                     tree: Optional[list] = None,
                     raw_schema: Optional[dict] = None
                     ):
  """Parses the cursor's key attributes and adds them to the schema."""

  # Allow for overriding the tree when recursing
  if not tree: tree = cursor['tree'].copy()

  # Attempt to fix values inconsistent with the sample plist
  if not nested_get(sample, tree):
    # 'Entry Properties' has an inconsistent name
    if tree == ['Misc', 'Entry']:
      tree[-1] = 'Entries'
      # These properties are also applicable to `Misc.Tools`
      _parse_key_entry(cursor, schema, sample,
                       tree=('Misc', 'Tools'),
                       raw_schema=raw_schema)
    # 'Memory Device Properties' has an inconsistent name
    if tree == ['PlatformInfo', 'Memory', 'Device']:
      tree[-1] = 'Devices'

  # Add entries to the schema
  entry_tree = _add_schema_entry(tree, cursor, schema)

  # If specified, add the raw LaTeX entry to the raw schema
  if entry_tree and raw_schema is not None:
    # Maps the entry tree to a <key>.<key>[idx].<key>... string
    tree = "".join(f'[{k}]' if isinstance(k, int) else f'.{k}'
                    for k in entry_tree)[1:]
    nested_set(raw_schema, (tree,), cursor['entry'])

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
    if   size := re_search(', (\\d+) bits?', stype, group=1):
      svalue = '0' * 1 * int(size)
    elif size := re_search(', (\\d+) bytes?', stype, group=1):
      svalue = '0' * 2 * int(size)
  elif atype in ('Dictionary'):
    atype = 'Dict'

  if svalue.lower().split(maxsplit=1)[0] in ('empty',):
    svalue = ''

  # Ensure value is serializable as an annotated YAML type
  value = parse_yaml_types(atype, svalue, schema='annotated')

  return value

def _add_schema_entry(tree: list, cursor: dict, schema: dict) -> List[str]:
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

  # Add entry to the schema
  if   isinstance(parent_entry, dict):
    entry_tree = (*tree, key)
    nested_set(schema, entry_tree, entry)
  elif isinstance(parent_entry, list):
    if not parent_entry: parent_entry = [{}]
    # Only one dict entry is allowed per array
    entry_tree = (*tree, 0, key)
    parent_entry[0][key] = entry
    nested_set(schema, tree, parent_entry)

  # Return the entry tree for validation
  return entry_tree

################################################################################
#                              Schema Parsing Methods                          #
################################################################################

def _is_boundary(lnorm: str, indent: str, entry: str) -> bool:
  """Checks if the line is a valid boundary command."""

  # Check if the line is a valid root command
  if lnorm[:1] == '\\' and indent <= 1:
    return True
  if not any(lnorm.startswith(c) for c in ('\\item', '\\end{enumerate}')):
    return False
  # Handle false positives for \item commands
  list_count = entry.count('\\begin{itemize}')
  is_building_list = list_count == 1 + entry.count('\\end{itemize}') > 0
  if lnorm != '\\item' or is_building_list:
    return False

  return True

def _is_nested_boundary(cursor: dict, indent: str, entry: str) -> bool:
  """Checks if the line is a valid nested boundary command."""

  # Handle false positives for nested \item commands
  if cursor['type'] and indent >= 2:
    trailing_command = entry.rstrip().rsplit(maxsplit=1)[-1]
    is_nested_list = trailing_command in ('\\begin{itemize}', '\\tightlist')
    has_finished_list = trailing_command == '\\end{itemize}'
    # Is still a nested key entry
    if not is_nested_list and has_finished_list:
      return False

  return True

def parse_schema(file: Union[List[str], TextIOWrapper],
                 sample_plist: dict,
                 /,
                 raw_schema: Optional[dict] = None
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
    raw_schema: If specified, the raw schema will be stored in this dictionary.

  Returns:
    A dictionary representing failsafe values for the Sample.plist schema.
  """

  # Parse the configuration schema against the sample plist
  cursor = { 'tree': [], 'key': None, 'type': None, 'value': None, 'entry': '' }
  schema = {}
  for line in file:
    # Normalize line
    lnorm = str(lstrip := line.lstrip()).strip()
    # Skip comments
    if lnorm[:1] == '%': continue

    # Use root-level commands as boundaries for key entries
    indent = len(line) - len(lstrip)
    if (entry := cursor['entry'] or '') and _is_boundary(lnorm, indent, entry):
      # Add value to the schema if all required attributes are present
      if cursor['key'] and cursor['type']:
        # Normalize entry to fix formatting inconsistencies
        if not _is_nested_boundary(cursor, indent, entry):
          cursor['entry'] += f"\n{line}"
        cursor['entry'] = _normalize_lines(entry)
        # Add entry to the schema
        _parse_key_entry(cursor, schema, sample_plist, raw_schema=raw_schema)
      # Reset all attributes
      _reset_key_entry(cursor)
    # If set, continue storing the current LaTeX entry
    elif entry:
      cursor['entry'] += f"\n{line}"

    # Parse LaTeX commands
    if command := _extract_command(lnorm):
      # Parse section/subsection commands
      if command in ('\\section', '\\subsection', '\\subsubsection'):
        name: str = re_search(f'\\{command}\\{{(.*?)\\}}', lnorm, group=1)
        # Is a section
        if command == '\\section':
          entry = [name] if name in sample_plist.keys() else []
          cursor['tree'] = entry
        # Is a subsection
        else:
          key = re_search(r'([a-zA-Z0-9]+)\s?Properties', name, group=1)
          if command == '\\subsection':
            entry = [key] if key else []
            cursor['tree'][1:] = entry
          elif command == '\\subsubsection':
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
