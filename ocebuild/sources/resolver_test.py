## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

import pytest

from pathlib import Path
from typing import TypeVar

from sources.resolver import *


def test_GitHubResolver():
  # Test release url resolution
  assert GitHubResolver(repository='acidanthera/RestrictEvents',
                        tag='~1.0.6'
                        ).resolve() == \
    'https://github.com/acidanthera/RestrictEvents/releases/tag/1.0.9'
  # Test raw file url resolution
  assert GitHubResolver(repository='acidanthera/RestrictEvents',
                        branch='force-vmm-install',
                        path='RestrictEvents/Info.plist'
                        ).resolve() == \
    'https://raw.githubusercontent.com/acidanthera/RestrictEvents/force-vmm-install/RestrictEvents/Info.plist'
  # Test artifact url resolution
  assert GitHubResolver(repository='acidanthera/RestrictEvents',
                        branch='force-vmm-install',
                        commit='e5c52564f5bca1aebbd916f2753f5a58809703a8'
                        ).resolve() == \
    'https://github.com/acidanthera/RestrictEvents/suites/13511383482/artifacts/742567994'
  # Test latest release url resolution
  assert GitHubResolver(repository='acidanthera/RestrictEvents').resolve()

def test_PathResolver():
  cls = type(Path())

  # Test BaseResolver and PathResolver subclassing
  assert PathResolver('example/build.lock').path == \
    'example/build.lock'
  assert dict(PathResolver('example/build.lock')) == \
    { 'path': 'example/build.lock' }

  # Test resolve() output (tests PathResolver bound method)
  for s in [
    'example/build.lock',
    'ocebuild/../example/build.lock'
  ]:
    assert str(PathResolver(s).resolve()) == str(cls(s).resolve())

  # Test absolute() output (tests PosixPath/WindowsPath bound method)
  for s in [
    'example/build.lock',
    'ocebuild/../example/build.lock'
  ]:
    assert str(PathResolver(s).absolute()) == str(cls(s).absolute())
