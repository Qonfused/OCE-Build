## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

import pytest

from .github import *


def test_github_file_url(): pass # Not implemented

def test_github_archive_url(): pass # Not implemented

def test_github_release_url(): pass # Not implemented

def test_github_artifacts_url():
  repository='acidanthera/RestrictEvents'
  commit='954bd4e21093bf059a15f8692e086586d5cb2dc6'
  url = github_artifacts_url(repository,
                             commit=commit)
  assert url == 'https://github.com/acidanthera/RestrictEvents/suites/13641781448/artifacts/752936784'
