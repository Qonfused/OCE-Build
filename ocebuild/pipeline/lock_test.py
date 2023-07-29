## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

import pytest

from .lock import *


def test_parse_semver_params():
  # Test resolution for tags
  assert parse_semver_params(None, '=2.2.0') == \
    {'tag': '2.2.0'}
  assert parse_semver_params(None, '#tag=2.2.0') == \
    {'tag': '2.2.0'}
  assert parse_semver_params(dict(tag='2.2.0'), 'foo/bar') == \
    {'tag': '2.2.0'}

  # Test resolution for branches
  assert parse_semver_params(None, '#master') == \
    {'branch': 'master'}
  assert parse_semver_params(None, '#branch=master') == \
    {'branch': 'master'}
  assert parse_semver_params(dict(branch='master'), 'foo/bar') == \
    {'branch': 'master'}

  # Test resolution for commits
  assert parse_semver_params(None, '#6b79b48') == \
    {'commit': '6b79b48'}
  assert parse_semver_params(None, '#commit=6b79b48') == \
    {'commit': '6b79b48'}
  assert parse_semver_params(dict(commit='6b79b48'), 'foo/bar') == \
    {'commit': '6b79b48'}
