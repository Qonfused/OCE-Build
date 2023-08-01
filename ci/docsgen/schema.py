#!/usr/bin/env python3

## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Documentation writers and parsers for OpenCore configuration file schemas."""

from collections import OrderedDict
from datetime import datetime, timezone
from json import dumps as json_dumps

from typing import Optional

from ci import PROJECT_DOCS, PROJECT_ROOT

from ocebuild.parsers.dict import flatten_dict, merge_dict, nested_get
from ocebuild.parsers.plist import write_plist
from ocebuild.parsers.regex import re_search
from ocebuild.parsers.schema import format_markdown_entry
from ocebuild.parsers.types import decode_data
from ocebuild.parsers.yaml import write_yaml
from ocebuild.pipeline.config import get_configuration_schema
from ocebuild.pipeline.lock import resolve_specifiers

from third_party.cpython.pathlib import Path


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


if __name__ == '__main__':
  entry = next(iter(resolve_specifiers({
    'OpenCorePkg': {
      'OpenCore': {
        'specifier': 'latest',
        'repository': 'acidanthera/OpenCorePkg',
        'build': 'RELEASE'
      },
    }
  }, lockfile={})), {})

  commit_sha = re_search('(?<=#commit=)[a-f0-9]+', entry.get('resolution'))
  schema, sample = get_configuration_schema(commit=commit_sha,
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


__all__ = [
  # Functions (1)
  "parse_fmarkdown_schema"
]
