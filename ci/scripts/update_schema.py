#!/usr/bin/env python3

## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Documentation writers and parsers for OpenCore configuration file schemas."""

from argparse import ArgumentParser
from collections import OrderedDict
from datetime import datetime, timezone
from json import dumps as json_dumps
from re import sub as re_sub

from typing import Optional

from ci import PROJECT_DOCS, PROJECT_ROOT

from ocebuild.parsers.dict import flatten_dict, merge_dict, nested_get
from ocebuild.parsers.plist import write_plist
from ocebuild.parsers.regex import re_search
from ocebuild.parsers.types import decode_data
from ocebuild.parsers.yaml import write_yaml
from ocebuild.pipeline.config import get_configuration_schema
from ocebuild.pipeline.lock import resolve_specifiers

from third_party.cpython.pathlib import Path


def format_markdown_entry(key: str, entry: str) -> str:
  """Formats a Sample.plist schema entry as markdown."""

  # Converts the key to a markdown header
  key_fmt = key \
    .replace('.', ' -> ') \
    .replace('[0]', '[]')
  header = '#' * (1 + key.count('.') + key.count('[]'))

  #TODO: Parse markdown tables, see Kernel -> Scheme -> KernelArch

  entry_keys = "|".join(['Type', 'Failsafe', 'Requirement', 'Description'])
  for pattern, repl in [
    # Properly space out entry keys
    (r'\\textbf\{(' + entry_keys + r')\}:', r'\n\n\n**\1**:'),
    # Add bold formatting to all bold text
    (r'\\textbf\{([^}]+)\}',  r'**\1**'),
    # Add italic formatting to all italic text
    (r'\\textit\{([^}]+)\}',  r'*\1*'),
    (r'\\emph\{([^}]+)\}',    r'*\1*'),
    # Add quote formatting to all quoted text
    (r'`([^`\']+)\'',         r"'\1'"),
    # Add strikethrough formatting to all strikethrough text
    (r'\\sout\{([^}]+)\}',    r'~~\1~~'),
    # Add monospace formatting to all teletype text
    (r'\\texttt\{([^}]+)\}',  r'`\1`'),
    # Handle anchor and alignment commands
    (r'\\medskip',            r''), #r'\n\n'),
    (r'\\label\{([^}]+)\}',   r''),
    (r'\\begin\{([^}]+)\}',   r'\n'),
    (r'\\end\{([^}]+)\}\n',   r''),
    # Handle named commands for special characters
    (r'\\textless\{?\}?',         r'\<'),
    (r'\\textgreater\{?\}?',      r'\>'),
    (r'\\textasciitilde\{?\}?',   r'~'),
    # Handle url links and header refs
    (r'\\href\{([^}]+)\}\{([^}]+)\}',       r'[\2](\1)'),
    (r'\\hyperref\[([^}]+)\]\{([^}]+)\}',   r'**\2**'), # r'[\2](#\1)'),
    (r'\\hyperlink\{([^}]+)\}\{([^}]+)\}',  r'**\2**'), # r'[\2](#\1)'),
    # Convert all lists to markdown bullets
    (r'\\begin\{itemize\}',   r'\n'),
    (r'\s*?\\tightlist',      r''),
    (r'\s*?\\item',           r'\n*'),
    (r'\n\\end\{itemize\}',   r''),
    # Handle escaped characters
    (r'\\([#%&_{}~^<>$ ])|\\\s',  r'\1'),
    # Handle invalid escapes/closures
    (r'\*\\ `',                       r'\n`'),
    (r'(:|`)\\ `',                    r'\1\n  * `'), # Kernel -> Emulate -> Cpuid1Data
    (r'\n\s*?\*?\s*?\`(OCAU|HDA)\:',  r'\n* `\1:'),  # UEFI -> Audio -> AudioCodec/AudioOutMask
    (r'\\\*\*',                       r' **'),
    (r' \\ \*',                       r'\n\n*'),
    (r'\\\`}\).',                     r'}`).'),      # PlatformInfo -> UseRawUuidEncoding
    # Handle escaped backslashes
    (r'\\\s?\n',              r'\n'),
    (r'\\textbackslash',      r'\\'),
    (r'\\\\',                 r'\\'),
    (r'\s?\\\s?',                  r'\\'),
  ]: entry = re_sub(pattern, repl, entry)

  start = entry.index('**Type**:')
  end = len(entry)

  #FIXME: Add a truncation point for invalid entries
  for block in ['\\hypertarget{kernmatch}']:
    if block in entry:
      end = min(end, entry.index(block))

  return f"{header} {key_fmt}\n\n{entry[start:end].strip()}"

def parse_fmarkdown_schema(raw_schema: dict,
                           schema: dict,
                           sample: dict,
                           /,
                           title: str='OpenCore Config.plist Schema',
                           metadata: Optional[dict]=None,
                           ) -> str:
  """Parses the raw schema into a flavoured markdown document.

  Args:
    raw_schema: The raw schema LaTeX AST to parse.
    schema: The Sample.plist schema to extract defaults from.
    sample: The Sample.plist to extract defaults from.
    title: The title of the document.
    metadata: Additional metadata to include in the document.

  Returns:
    A flavoured markdown document representing the schema.
  """

  flat_schema = flatten_dict(schema)
  flat_sample = flatten_dict(sample)

  table_of_contents = '<h2 id=table-of-contents>Table of Contents</h2>'
  table_of_contents += '\n\n<details><summary>Click to Expand</summary>\n'

  document = ''

  for key, entry in sorted(raw_schema.items()):
    entry_fmt = format_markdown_entry(key, entry)

    # Add friendlier anchor links for each entry
    # E.g. 'ACPI -> Add[] -> Comment' -> '#acpi-add-comment'
    level, name = re_search(r'^([#]*)\s+(.*?)$', entry_fmt, None, True).groups()
    slug = str(name) \
      .replace(' -> ', '-') \
      .replace('[]', '') \
      .lower()
    header = f'<h{len(level)} id={slug}>{name}</h{len(level)}>'
    entry_fmt = "\n".join([header, *entry_fmt.split('\n')[1:]])

    # Add entry to the table of contents
    list_indent = ' ' * 2 * (len(level) - 2)
    table_of_contents += f'\n{list_indent}- [{name}](#{slug})'

    # Extract defaults from Sample.plist or Schema.plist
    default = nested_get(flat_sample, (key,), default=None)
    if default is not None and '[]' in name:
      default = nested_get(flat_schema, (key,), default=None)

    # Add a default value to the entry
    if default is not None:
      if isinstance(default, (str, bytes)) and not len(default):
        default = 'Empty'
      elif isinstance(default, str) and len(default):
        default = f"`{default}`"
      elif isinstance(default, bytes) and len(default):
        default = f"`0x{decode_data(default, enc='hex')}`"
      elif isinstance(default, bool):
        default = f"`{str(default).lower()}`"
      elif isinstance(default, (int, float)):
        default = f"`{default}`"
      elif isinstance(default, dict):
        default = '`plist dict`' if default else 'Empty'
      elif isinstance(default, list):
        default = '`plist array`' if default else 'Empty'

      # Insert default value before the failsafe value.
      entry_fmt = entry_fmt \
        .replace(ins := '**Failsafe**:', f'**Default**: {default}\n\n{ins}')

    document += f"\n\n{entry_fmt.rstrip()}"

  header = f'<h1 id=schema>{title}</h1>'
  # Add metadata to the header
  if metadata is not None:
    version = metadata.get('version', 'Unknown')
    timestamp = datetime.now(tz=timezone.utc)
    revision = metadata.get('revision', 'Unknown')

    header = f"<h1 id=schema>{title} - v{version}</h1>"
    header += f"\n\n#### Last Updated: `{timestamp}`\n"
    header += f"\n#### Revision: `{revision}`"

  table_of_contents += '\n\n</details>'
  document = f"{header}\n\n{table_of_contents}{document}"

  return document


def _main(tag: Optional[str]=None, commit: Optional[str]=None) -> None:
  """Generates the OpenCore configuration schema documentation."""

  parameters = {
    'specifier': 'latest',
    'repository': 'acidanthera/OpenCorePkg',
    'build': 'RELEASE'
  }
  if tag:
    parameters['tag'] = tag
  if commit:
    parameters['commit'] = commit

  # Build a resolver entry reflecting the specified OpenCore version
  entry = next(iter(resolve_specifiers({
    'OpenCorePkg': {
      'OpenCore': parameters,
    }
  }, lockfile={})), {})
  if not (tag or commit):
    commit = re_search('(?<=#commit=)[a-f0-9]+', entry.get('resolution'))

  # Retrieve the configuration schema and sample plist
  schema, sample = get_configuration_schema(tag=tag,
                                            commit=commit,
                                            raw_schema=(raw_schema := {}),
                                            get_sample=True)
  schema_meta = OrderedDict(**{
    '#Revision': {
      'OpenCore-Version': entry.get('version', 'Unknown'),
    }
  })

  schema_dict = merge_dict(schema_meta, schema)
  with open(PROJECT_DOCS.joinpath('resources', 'Schema.plist'), 'w') as file:
    schema_plist = write_plist(merge_dict(schema_meta, schema))
    file.write(schema_plist)
  with open(PROJECT_DOCS.joinpath('resources', 'Schema.yaml'), 'w') as file:
    schema_yaml = "\n".join(write_yaml(schema_dict, schema='annotated'))
    file.write(schema_yaml)

  with open(PROJECT_DOCS.joinpath('schema.md'), 'w') as file:
    schema_doc = parse_fmarkdown_schema(raw_schema, schema, sample,
                                        title="OpenCore Config.plist Schema",
                                        metadata=entry)
    file.write(schema_doc)

  # Update registry version for schema
  registry_vers = Path(PROJECT_ROOT, 'ci', 'registry', 'schema.json')
  registry_vers.write_text(json_dumps({ 'version': entry.get('version') }))


if __name__ == '__main__':
  parser = ArgumentParser()
  parser.add_argument('--tag',
                      nargs='?',
                      help='The OpenCore tag to use.')
  parser.add_argument('--commit',
                      nargs='?',
                      help='The OpenCore commit to use.')
  args = parser.parse_args()

  _main(tag=args.tag, commit=args.commit)


__all__ = [
  # Functions (2)
  "format_markdown_entry",
  "parse_fmarkdown_schema"
]
