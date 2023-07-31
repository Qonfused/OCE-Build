## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

from pathlib import Path

import pytest

from .resolver import *


def test_GitHubResolver():
  # Test release asset url resolution
  assert GitHubResolver(repository='OpenIntelWireless/itlwm',
                        tag='2.2.0',
                        __name__='AirportItlwm-BigSur').resolve() == \
    'https://github.com/OpenIntelWireless/itlwm/releases/download/v2.2.0/AirportItlwm_v2.2.0_stable_BigSur.kext.zip'
  # Test release url resolution
  assert GitHubResolver(repository='acidanthera/RestrictEvents',
                        tag='~1.0.6'
                        ).resolve() == \
    'https://github.com/acidanthera/RestrictEvents/releases/tag/1.0.9'
  # Test raw file url resolution
  assert GitHubResolver(repository='Qonfused/DiskArbitrationFixup',
                        branch='master',
                        path='DiskArbitrationFixup/Info.plist'
                        ).resolve() == \
    'https://raw.githubusercontent.com/Qonfused/DiskArbitrationFixup/5670dddc49cfaf5b5fb54b0335f98a4df7ada1a0/DiskArbitrationFixup/Info.plist'
  #FIXME: Test artifact url resolution
  # assert GitHubResolver(repository='acidanthera/RestrictEvents',
  #                       branch='force-vmm-install',
  #                       commit='e5c52564f5bca1aebbd916f2753f5a58809703a8'
  #                       ).resolve() == \
  #   'https://github.com/acidanthera/RestrictEvents/suites/13511383482/artifacts/742567994'
  # Test latest release url resolution
  assert GitHubResolver(repository='acidanthera/RestrictEvents',
                        branch='master').resolve()

def test_DortaniaResolver(): pass # Not implemented

def test_PathResolver():
  cls = type(Path())

  # Test BaseResolver and PathResolver subclassing
  assert PathResolver('docs/example/src/build.lock').path == \
    'docs/example/src/build.lock'
  assert dict(PathResolver('docs/example/src/build.lock')) == \
    { 'path': 'docs/example/src/build.lock' }

  # Test resolve() output (tests PathResolver bound method)
  for s in [
    'docs/example/src/build.lock',
    'ocebuild/../docs/example/src/build.lock'
  ]:
    assert str(PathResolver(s).resolve()) == str(cls(s).resolve())

  # Test absolute() output (tests PosixPath/WindowsPath bound method)
  for s in [
    'docs/example/src/build.lock',
    'ocebuild/../docs/example/src/build.lock'
  ]:
    assert str(PathResolver(s).absolute()) == str(cls(s).absolute())
