## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

from pathlib import Path
from unittest.mock import patch, MagicMock

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
  # # Test latest release url resolution
  # assert GitHubResolver(repository='acidanthera/RestrictEvents',
  #                       branch='master').resolve()


def test_extract_asset_preserves_build_target():
  """Test that RELEASE/DEBUG build target is preserved in all fallback paths."""
  from unittest.mock import patch
  
  # Mock release catalog with BrcmPatchRAM-like assets (bundled kexts)
  mock_catalog = {
    'assets': [
      {'name': 'BrcmPatchRAM-2.7.2-RELEASE.zip', 'browser_download_url': 'https://example.com/RELEASE.zip'},
      {'name': 'BrcmPatchRAM-2.7.2-DEBUG.zip', 'browser_download_url': 'https://example.com/DEBUG.zip'},
    ],
    'tag_name': '2.7.2'
  }
  
  with patch('ocebuild.sources.github.github_release_catalog', return_value=mock_catalog):
    resolver = GitHubResolver(repository='acidanthera/BrcmPatchRAM', __name__='BlueToolFixup')
    
    # Request RELEASE - should get RELEASE
    url = resolver.extract_asset(resolver, 'BlueToolFixup', 'https://example.com/releases/tag/2.7.2', build='RELEASE')
    assert 'RELEASE' in url
    assert 'DEBUG' not in url
    
    # Request DEBUG - should get DEBUG
    url = resolver.extract_asset(resolver, 'BlueToolFixup', 'https://example.com/releases/tag/2.7.2', build='DEBUG')
    assert 'DEBUG' in url
    assert 'RELEASE' not in url


def test_extract_asset_fails_when_build_unavailable():
  """Test that resolution fails when requested build is not available."""
  from unittest.mock import patch
  
  # Mock release catalog with only DEBUG assets
  mock_catalog = {
    'assets': [
      {'name': 'BrcmPatchRAM-2.7.2-DEBUG.zip', 'browser_download_url': 'https://example.com/DEBUG.zip'},
    ],
    'tag_name': '2.7.2'
  }
  
  with patch('ocebuild.sources.github.github_release_catalog', return_value=mock_catalog):
    resolver = GitHubResolver(repository='acidanthera/BrcmPatchRAM', __name__='BlueToolFixup')
    
    # Request RELEASE but only DEBUG available - should fail
    try:
      resolver.extract_asset(resolver, 'BlueToolFixup', 'https://example.com/releases/tag/2.7.2', build='RELEASE')
      assert False, "Should have raised ValueError"
    except ValueError as e:
      assert 'No RELEASE asset found' in str(e)
      assert 'DEBUG' in str(e)


def test_extract_asset_name_match_no_build_indicator():
  """Test fallback when assets have name match but no build indicator."""
  from unittest.mock import patch
  
  # Mock release catalog with assets that match name but no build indicator
  mock_catalog = {
    'assets': [
      {'name': 'MyKext-1.0.0.zip', 'browser_download_url': 'https://example.com/MyKext-1.0.0.zip'},
    ],
    'tag_name': '1.0.0'
  }
  
  with patch('ocebuild.sources.github.github_release_catalog', return_value=mock_catalog):
    resolver = GitHubResolver(repository='acidanthera/MyKext', __name__='MyKext')
    
    # Should work when no build indicator present
    url = resolver.extract_asset(resolver, 'MyKext', 'https://example.com/releases/tag/1.0.0', build='RELEASE')
    assert 'MyKext-1.0.0.zip' in url


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
