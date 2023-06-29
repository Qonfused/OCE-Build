## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

import pytest

from parsers.dict import nested_get
from parsers.yaml import *


def test_parse_serialized_types(): pass # Not implemented

def test_write_serialized_types(): pass # Not implemented

def test_parse_yaml():
  # Verify no list mutability pollution
  parse_yaml(lines=['#foo'], config={'foo': 'bar'}, flags=['foo'])
  assert not parse_yaml(lines=[])
  assert not parse_yaml(lines=[], config={}, flags=[])

  # Validate parsing TextIOWrapper input
  file = open('docs/example/build.yml', 'r', encoding='UTF-8')
  assert parse_yaml(file)
  file = open('example/build.lock', 'r', encoding='UTF-8')
  assert parse_yaml(file)
  
  # Validate parsing List[str] input
  file = open('docs/example/build.yml', 'r', encoding='UTF-8')
  assert parse_yaml(lines=[l.rstrip() for l in file])
  file = open('example/build.lock', 'r', encoding='UTF-8')
  lockfile = parse_yaml(lines=[l.rstrip() for l in file])
  assert lockfile

  # Validate parsing frontmatter
  file = open('docs/example/build.yml', 'r', encoding='UTF-8')
  output, frontmatter = parse_yaml(lines=[l.rstrip() for l in file],
                                   frontmatter=True)
  assert output
  assert frontmatter

  # Validate known lockfile schema
  for entry in lockfile:
    keys = lockfile[entry].keys()
    for k in keys:
      assert nested_get(lockfile, [entry, k]) is not None
    assert 'checksum' in keys
    assert 'resolution' in keys
    assert 'url' in keys
    assert 'version' in keys
    if 'extract' in keys:
      arr = nested_get(lockfile, [entry, 'extract'])
      assert (isinstance(arr, str) or isinstance(arr, list)) and len(arr)

def test_write_yaml(): pass # Not implemented
