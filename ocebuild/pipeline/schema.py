## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Methods for retrieving and handling Sample.plist schemas."""

from functools import partial

from typing import Union

from ocebuild.parsers.dict import nested_get, nested_set
from ocebuild.parsers.plist import parse_plist
from ocebuild.parsers.regex import re_search
from ocebuild.parsers.yaml import parse_yaml_types
from ocebuild.sources import request
from ocebuild.sources.github import github_file_url


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

def _parse_key_entry(cursor: dict, schema: dict, sample: dict):
  """Add value to the schema if all required attributes are present"""
  if (key := cursor['key']) and (stype := cursor['type']):

    # Set default allowlist based on parent key
    valid = set(cursor['tree'][-1:])
    invalid = set()

    # Parse description for any inconsistencies
    if desc := cursor['description']:
      desc = desc \
        .replace('\n\n', '<\\n\\n>') \
        .replace('\n', ' ') \
        .replace('<\\n\\n>', '\n\n')
      cursor['description'] = desc

      # Parse description for exclusion/inclusion rules
      valid_pattern = r'\\emph\{Note\}: This option is only valid for \\texttt\{(.*?)\}'
      if valid_match := re_search(valid_pattern, desc, group=1):
        valid = set((valid_match,))
      invalid_pattern = valid_pattern + r' and cannot be specified for \\texttt\{(.*?)\}'
      if invalid_match := re_search(invalid_pattern, desc, group=2):
        invalid = set((invalid_match,))

    def add_entry(tree: list):
      """Parse and add failsafe values"""

      # Ensure that the parent entry is a valid target
      nonlocal valid, invalid; pkey = tree[-1]
      if pkey not in valid and pkey in invalid: return

      # Parse failsafe value
      nonlocal key, stype; svalue = cursor['value'] or 'Empty'
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

    # Attempt to fix values inconsistent with the sample plist
    tree = cursor['tree'].copy()
    try:
      if not nested_get(sample, tree):
        # 'Entry Properties' has an inconsistent name
        if tree == ['Misc', 'Entry']:
          tree[-1] = 'Entries'
          # These properties are also applicable to `Misc.Tools`
          add_entry(('Misc', 'Tools'))
        # 'Memory Device Properties' has an inconsistent name
        if tree == ['PlatformInfo', 'Memory', 'Device']:
          tree[-1] = 'Devices'
        else:
          raise KeyError(tree[-1])
    except: pass

    # Add entry to the schema
    add_entry(tree)

  # Reset values
  cursor['key'] = None
  cursor['type'] = None
  cursor['value'] = None
  cursor['description'] = None

def get_configuration_schema(repository: str='acidanthera/OpenCorePkg',
                             branch: str = 'master',
                             tag: Union[str, None] = None,
                             commit: Union[str, None] = None,
                             ) -> dict:
  """Gets the configuration schema from a Configuration.tex file."""

  # Resolve file urls for the given repository parameters.
  file_url = partial(github_file_url,
                     repository=repository,
                     branch=branch,
                     tag=tag,
                     commit=commit,
                     raw=True)

  # Get the reference configuration and sample plist urls
  configuration_url = file_url(path='Docs/Configuration.tex')
  sample_plist_url = file_url(path='Docs/Sample.plist')

  # Parse the configuration schema against the sample plist
  schema = {}
  sample_plist = parse_plist(request(url=sample_plist_url).text())
  parse_key_entry = partial(_parse_key_entry,
                            schema=schema,
                            sample=sample_plist)

  with request(url=configuration_url).text() as file:
    cursor = {
      'tree': [],
      'key': None,
      'type': None,
      'value': None,
      'description': None
    }
    for line in file:
      # Parse LaTeX commands
      lnorm = str(line).strip()
      if lnorm[:1] == '\\' and (command := lnorm.split('{', 1)[0])[1:]:
        # Handle match on labels, etc
        if command.count('\\') > 1:
          command = command.split(maxsplit=1)[0]
        # Parse section/subsection commands
        if command in ('\section', '\subsection', '\subsubsection'):
          name: str = re_search(f'\\{command}\{{(.*?)\}}', lnorm, group=1)
          if cursor['key']: parse_key_entry(cursor)
          # Is a section
          if command == '\section':
            if name in sample_plist.keys():
              cursor['tree'] = [name]
            else:
              cursor['tree'] = []
              continue
          # Is a subsection
          elif command == '\subsection':
            if key := re_search(r'([a-zA-Z0-9]+)\s?Properties', name, group=1):
              cursor['tree'][1:] = [key]
            else:
              cursor['tree'][1:] = []
              continue
          elif command == '\subsubsection':
            if key := re_search(r'([a-zA-Z0-9]+)\s?Properties', name, group=1):
              key = key.split(maxsplit=1)[0]
              cursor['tree'][2:] = [key]
            else:
              cursor['tree'][2:] = []
              continue
        elif not cursor['tree']: continue
        # Parse property fields for keys
        elif not cursor['description'] and command in ('\\texttt', '\\textbf'):
          if   command == '\\texttt':
            # Is a key name
            if key := _extract_key(command, lnorm, sol=''):
              if not cursor['key']: cursor['key'] = key
          elif command == '\\textbf':
            # Is a key type
            if   stype := _extract_value(command, lnorm, key='Type'):
              cursor['type'] = stype
              # Append any additional attributes
              stype = stype.replace('\\', '\\\\')
              attr_pattern = f'\{{{stype}\}},?\s?(.*?)\\\\\\\\$'
              if attr := re_search(attr_pattern, lnorm, group=1):
                cursor['type'] += f", {attr}"
            # Is a key value
            elif svalue := _extract_value(command, lnorm, key='Failsafe'):
              cursor['value'] = svalue
            # Is a key description
            elif desc := _extract_value(command, lnorm, key='Description', eol=''):
              cursor['description'] = desc
              continue
        # Reset cursor on item boundaries
        elif command == '\item':
          parse_key_entry(cursor)
      # Continue parsing descriptions
      if cursor['description']:
        cursor['description'] += f"\n{lnorm}"

  return schema


__all__ = [
  # Functions (1)
  "get_configuration_schema"
]
