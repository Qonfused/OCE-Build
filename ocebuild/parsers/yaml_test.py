## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

from datetime import datetime, timezone

import pytest

from .dict import nested_get
from .yaml import *

from ci import PROJECT_DOCS, PROJECT_EXAMPLES


SIMPLE_DEMO = PROJECT_EXAMPLES.joinpath('simple-demo-project', 'src')

def test_parse_yaml_types(): pass # Not implemented

def test_write_yaml_types():
  # Handle annotated schema
  assert write_yaml_types([],
                                schema='annotated') == \
    ('Array  ', '(empty)')
  assert write_yaml_types(('data', b'\x01\x00\x00\x00'),
                                schema='annotated') == \
    ('Data   ', '<01000000>')
  assert write_yaml_types(('date', datetime(2020, 1, 1, 0, 0, tzinfo=timezone.utc)),
                                schema='annotated') == \
    ('Date   ', "2020-01-01T00:00:00Z")
  assert write_yaml_types({},
                                schema='annotated') == \
    ('Dict   ', '(empty)')
  assert write_yaml_types(('float', 1.0),
                                schema='annotated') == \
    ('Number ', '1.0')
  assert write_yaml_types(('int', 1),
                                schema='annotated') == \
    ('Number ', '1')
  assert write_yaml_types(('string', 'Foo'),
                                schema='annotated') == \
    ('String ', '"Foo"')
  assert write_yaml_types(('bool', True),
                                schema='annotated') == \
    ('Boolean', 'true')
  assert write_yaml_types(('bool', False),
                                schema='annotated') == \
    ('Boolean', 'false')

  # TODO: YAML schema tests

def test_parse_yaml():
  # Verify no list mutability pollution
  parse_yaml(lines=['#foo'], config={'foo': 'bar'}, flags=['foo'])
  assert not parse_yaml(lines=[])
  assert not parse_yaml(lines=[], config={}, flags=[])

  # Validate parsing TextIOWrapper input
  file = open(SIMPLE_DEMO.joinpath('build.yml'), 'r', encoding='UTF-8')
  assert parse_yaml(file)
  file.seek(0)
  assert parse_yaml(file)

  # Validate parsing List[str] input
  file = open(SIMPLE_DEMO.joinpath('build.yml'), 'r', encoding='UTF-8')
  assert parse_yaml(lines=[l.rstrip() for l in file])
  file.seek(0)
  lockfile = parse_yaml(lines=[l.rstrip() for l in file])
  assert lockfile

  # Validate parsing frontmatter
  file = open(SIMPLE_DEMO.joinpath('build.yml'), 'r', encoding='UTF-8')
  output, frontmatter = parse_yaml(lines=[l.rstrip() for l in file],
                                   frontmatter=True)
  assert output
  assert frontmatter

  # Validate parsing plist schema
  file = open(PROJECT_DOCS.joinpath('resources', 'base-config.yml'), 'r',
              encoding='UTF-8')
  assert parse_yaml(file, frontmatter=True)

  # Validate handling preprocessor flags
  file.seek(0)
  output = parse_yaml(file,
                      flags=['RELEASE'])
  assert output
  assert not nested_get(output, ['Misc', 'Debug', 'AppleDebug'])
  file.seek(0)
  output = parse_yaml(file,
                      flags=['DEBUG'])
  assert output
  assert nested_get(output, ['Misc', 'Debug', 'AppleDebug'])

  # Validate known lockfile schema
  assert (kext_entries := lockfile['Kexts'])
  for entry in kext_entries:
    if isinstance(entry, dict):
      keys = entry.keys()
      for k in keys:
        assert nested_get(kext_entries, [entry, k]) is not None
      assert 'checksum' in keys
      assert 'resolution' in keys
      assert 'url' in keys
      assert 'version' in keys
      if 'extract' in keys:
        arr = nested_get(kext_entries, [entry, 'extract'])
        assert (isinstance(arr, str) or isinstance(arr, list)) and len(arr)
    else:
      assert entry is not None

def test_write_yaml(): pass # Not implemented
