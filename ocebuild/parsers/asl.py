## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Helper functions for parsing ASL source code."""

from collections import OrderedDict
from io import TextIOWrapper

from typing import List, Union

from .dict import nested_set
from .regex import re_search


def _normalize_line(string: str):
  """Normalizes a line of ASL source code."""
  return string \
    .replace('_', '') \
    .replace('"', '') \
    .replace("'", '')

def _normalize_scope(stmt: str,
                     name: str,
                     cursor: dict
                     ) -> str:
  """Normalizes the scope of a symbol's device path tree."""
  scope = cursor['scope']
  if any(c.startswith(ASL_PREFIX_MODIFIERS) for c in name):
    # Leave root-prefixed name unmodified
    if name[0] == ('\\'): return name[1:]
    # Handle upleveling cursor scope
    elif (uplevel := name.count('^')):
      name = name[uplevel:]
      scope = '.'.join(scope.split('.')[:-uplevel])
      # Modify cursor if statement is a scope
      if stmt == 'Scope': cursor['scope'] = scope
  # Resolve name scope
  delimiter = '.' if scope != '\\' else ''
  return delimiter.join([scope, name]) if scope else name

################################################################################
#                            ASL Directives and Opcodes                        #
################################################################################

ASL_COMPILER_CONTROLS = ( 'External', 'Include' )
"""Types of AST nodes that represent compiler controls.

For ASL Compiler Controls (19.16; Table), see:
https://uefi.org/htmlspecs/ACPI_Spec_6_4_html/19_ASL_Reference/ACPI_Source_Language_Reference.html#asl-compiler-controls
"""

ASL_TYPES_SCOPES = ( 'DefinitionBlock', 'Scope' )
"""Types of AST nodes that represent scopes."""

ASL_TYPES_CONDITIONALS = ( 'If', 'ElseIf', 'Else' )
"""Types of AST nodes that represent conditionals."""

ASL_PREFIX_MODIFIERS = ( '\\', '^' )
"""ASL name modifier prefixes.

For Definition Block Name Modifier Encodings (19.3; Table), see:
https://uefi.org/htmlspecs/ACPI_Spec_6_4_html/19_ASL_Reference/ACPI_Source_Language_Reference.html#definition-block-name-modifier-encodings

Example:
  ```cpp
  Scope (\\PCI0)
  {
    Name (X, 3)
    Scope (\\)
    {
      Method (RQ) {Return (0)}
    }
    Name (^Y, 4)
  }
  ```
  # ACPI Namespace -> PCI0.X, RQ, Y
"""

################################################################################
#                              ASL Block Arguments                             #
################################################################################

DEFINITION_BLOCK_ARGS = (
  'AMLFileName',
  'TableSignature',
  'ComplianceRevision',
  'OEMID',
  'TableID',
  'OEMRevision'
)
"""The arguments of a definition block.

For DefinitionBlock (19.6.29), see:
https://uefi.org/htmlspecs/ACPI_Spec_6_4_html/19_ASL_Reference/ACPI_Source_Language_Reference.html#definitionblock-declare-definition-block
"""

################################################################################
#                              Regular Expressions                             #
################################################################################

RE_BLOCK_ARGS = r'\(((?:.*?),?\s?)\)'
"""Regular expression for matching block arguments.

Groups:
  0: The matched line
  1: The block arguments
"""

RE_IMPORT_TYPE = r'\(.*?,\s?([a-zA-Z]+),?\)?'
"""Regular expression for matching import types.

For External (Declare External Objects, 19.6.45), see:
https://uefi.org/htmlspecs/ACPI_Spec_6_4_html/19_ASL_Reference/ACPI_Source_Language_Reference.html#external-declare-external-objects

Groups:
  0: The import type
"""

RE_LOCAL_VAR = r'^(Arg|Local)(\d+)$'
"""Regular expression for matching local-scoped object names.

For ArgX Objects (19.3.5.8.1), see:
https://uefi.org/htmlspecs/ACPI_Spec_6_4_html/19_ASL_Reference/ACPI_Source_Language_Reference.html#argx-objects

For LocalX Objects (19.3.5.8.2), see:
https://uefi.org/htmlspecs/ACPI_Spec_6_4_html/19_ASL_Reference/ACPI_Source_Language_Reference.html#localx-objects

Groups:
  0: The object type
  1: The variable index
"""

RE_STATEMENT = r'^([a-zA-Z]+)\s?\((.*?)[,\)]+?'
"""Regular expression for matching statements.

Groups:
  0: The statement type.
  1: The object name.
"""

RE_NAME = r'^[A-Z\^\_\\][a-zA-Z0-9\^\_\.\\]+$'
"""Regular expression for matching object names.

Groups:
  0: The object name.
"""

################################################################################
#                              ASL Parsing Methods                             #
################################################################################

def parse_definition_block(string: str) -> OrderedDict:
  """Parses arguments from a definition block line.

  Args:
    string: A definition block line.

  Returns:
    A dictionary of definition block arguments.

  Raises:
    ValueError: If the line is not a valid definition block.

  Example:
    >>> parse_definition_block('DefinitionBlock ("", "DSDT", 2, "_ASUS_", ...)')
    OrderedDict([('AMLFileName', ''),
                 ('TableSignature', 'DSDT'),
                 ('ComplianceRevision', 2),
                 ('OEMID', '_ASUS_'),
                 ('TableID', 'Notebook'),
                 ('OEMRevision', '0x01072009')])
  """
  definition_block = OrderedDict()
  # Validate definition block line
  args = re_search(RE_BLOCK_ARGS, string, group=1, multiline=True)
  if not args:
    raise ValueError(f'Invalid definition block: {string}')

  # Extract definition block arguments
  args = map(_normalize_line, args.split(', '))
  for arg, v in zip(DEFINITION_BLOCK_ARGS, args):
    # Parse `ComplianceVersion` arg as integer
    #  [0-1]: All integers are 32 bit
    #  [2+]:  All integers are 64 bit
    if arg == 'ComplianceRevision': v = int(v)
    else: v = _normalize_line(v)
    # Update definition block
    definition_block[arg] = v

  return definition_block

def parse_ssdt_namespace(lines: Union[List[str], TextIOWrapper]) -> dict:
  """Parses an SSDT's namespace for imports and statement exports.

  Args:
    lines: A list of SSDT lines.

  Returns:
    A dictionary of extracted SSDT information.

  Example:
    >>> parse_ssdt_namespace(open('path/to/ssdt.dsl', encoding='UTF-8'))
    >>> with open('path/to/ssdt.dsl', encoding='UTF-8') as ssdt_file:
    ...   ssdt_lines = [f.strip() for f in ssdt_file.readlines()]
    ...   parse_ssdt_namespace(ssdt_lines)
  """
  extracted = {
    'definition_block': OrderedDict(),
    'imports': OrderedDict(),
    'statements': OrderedDict(),
  }
  # Enumerate SSDT lines
  cursor = { 'scope': '', 'blocks': [] }
  for line in lines:
    # Skip empty lines
    if not (lnorm := line.lstrip()):
      continue
    # Skip comments
    if any(lnorm.startswith(c) for c in ('/*','*','*/', '//')):
      continue
    level = len(line[:-len(lnorm)])

    # Handle nested block and statement scopes
    if cursor['blocks'] and cursor['blocks'][-1][0] == level:
      if lnorm.startswith('{'): continue
      cursor['blocks'] = cursor['blocks'][:-1]
    # Handle downleveling cursor scope
    elif cursor['blocks'] and (downlevel := cursor['blocks'][-1][0] - level) >0:
      cursor['blocks'] = cursor['blocks'][:-downlevel]
    # Update cursor scope for subsequent entries
    else:
      cursor['scope'] = cursor['blocks'][-1][1] if cursor['blocks'] else ''

    # Extract tokens from line.
    ln_match = re_search(RE_STATEMENT, lnorm, group=None, multiline=True)
    if not ln_match: continue
    stmt, name = map(_normalize_line, ln_match.groups())
    # Skip local variables
    if re_search(RE_LOCAL_VAR, name): continue

    # Handle compiler control operators
    if stmt in ASL_COMPILER_CONTROLS:
      # Extract SSDT imports
      if stmt == 'External':
        import_type = re_search(RE_IMPORT_TYPE, lnorm, group=1, multiline=True)
        normalized_name = _normalize_scope(stmt, name,
                                           cursor={ 'scope': '', 'blocks': [] })
        nested_set(extracted, ['imports', normalized_name], import_type)
      # Include another SSDT file
      if stmt == 'Include': pass #pragma: no cover
      continue

    # Normalize object scope
    normalized_name = _normalize_scope(stmt, name, cursor)
    # Handle scopes types
    if stmt in ASL_TYPES_SCOPES:
      # Extract definition block
      if   stmt == 'DefinitionBlock':
        extracted['definition_block'] = parse_definition_block(lnorm)
      # Extract scope block
      elif stmt == 'Scope':
        cursor['blocks'].append((level, normalized_name))
      continue

    # Check if line is a statement
    if stmt in ASL_TYPES_CONDITIONALS: continue
    if name != re_search(RE_NAME, name): continue
    # Extract statement block
    nested_set(extracted, ['statements', normalized_name], stmt)
    cursor['blocks'].append((level, normalized_name))

  return extracted


__all__ = [
  # Constants (10)
  "ASL_COMPILER_CONTROLS",
  "ASL_TYPES_SCOPES",
  "ASL_TYPES_CONDITIONALS",
  "ASL_PREFIX_MODIFIERS",
  "DEFINITION_BLOCK_ARGS",
  "RE_BLOCK_ARGS",
  "RE_IMPORT_TYPE",
  "RE_LOCAL_VAR",
  "RE_STATEMENT",
  "RE_NAME",
  # Functions (2)
  "parse_definition_block",
  "parse_ssdt_namespace"
]
