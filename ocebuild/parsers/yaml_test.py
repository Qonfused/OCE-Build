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
  from io import TextIOWrapper

  from sources._lib import request
  from sources.github import github_file_url

  url = github_file_url('Qonfused/ASUS-ZenBook-Duo-14-UX481-Hackintosh',
                        path='src/build.lock',
                        raw=True)
  # with TextIOWrapper(request(url), encoding='utf-8') as file:
  with request(url).text(encoding='utf-8') as file:
    lockfile = parse_yaml([l.rstrip() for l in file])
    for entry in lockfile:
      # Enumerate entry keys
      keys = lockfile[entry].keys()
      for k in keys:
        assert nested_get(lockfile, [entry, k]) is not None
      assert 'checksum' in keys
      assert 'resolution' in keys
      assert 'url' in keys
      assert 'version' in keys
      if 'extract' in keys:
        arr = nested_get(lockfile, [entry, 'extract'])
        assert isinstance(arr, Union[str, list]) and len(arr)

def test_write_yaml(): pass # Not implemented
