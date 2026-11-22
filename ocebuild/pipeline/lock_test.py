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


def test_validate_dependencies_wildcard_bundle():
  """Test that lock --check passes for wildcard bundle entries."""
  # Simulate a lockfile with wildcard parent and materialized children
  lockfile = {
    'dependencies': {
      'Kexts': {
        'VirtualSMC': {
          'name': 'VirtualSMC',
          'specifier': 'latest',
          'version': '1.3.2',
          'url': 'https://github.com/acidanthera/VirtualSMC/releases/download/1.3.2/VirtualSMC-1.3.2-RELEASE.zip',
          'build': 'RELEASE',
          'kind': 'Kext',
          'resolution': 'acidanthera/VirtualSMC@github:1.3.2#checksum=abc123',
        },
        'SMCBatteryManager': {
          'name': 'SMCBatteryManager',
          'specifier': '*',
          'version': '1.3.2',
          'url': 'https://github.com/acidanthera/VirtualSMC/releases/download/1.3.2/VirtualSMC-1.3.2-RELEASE.zip',
          'build': 'RELEASE',
          'kind': 'Kext',
          'resolution': 'acidanthera/VirtualSMC@github:1.3.2#checksum=abc123',
          '_wildcard_parent': 'VirtualSMC',
        },
        'SMCLightSensor': {
          'name': 'SMCLightSensor',
          'specifier': '*',
          'version': '1.3.2',
          'url': 'https://github.com/acidanthera/VirtualSMC/releases/download/1.3.2/VirtualSMC-1.3.2-RELEASE.zip',
          'build': 'RELEASE',
          'kind': 'Kext',
          'resolution': 'acidanthera/VirtualSMC@github:1.3.2#checksum=abc123',
          '_wildcard_parent': 'VirtualSMC',
        },
        'SMCProcessor': {
          'name': 'SMCProcessor',
          'specifier': '*',
          'version': '1.3.2',
          'url': 'https://github.com/acidanthera/VirtualSMC/releases/download/1.3.2/VirtualSMC-1.3.2-RELEASE.zip',
          'build': 'RELEASE',
          'kind': 'Kext',
          'resolution': 'acidanthera/VirtualSMC@github:1.3.2#checksum=abc123',
          '_wildcard_parent': 'VirtualSMC',
        },
      }
    }
  }

  # Build config with wildcard children
  build_config = {
    'Kexts': {
      'VirtualSMC': {
        'specifier': 'latest',
      },
      'SMCBatteryManager': {
        'specifier': '*',
      },
      'SMCLightSensor': {
        'specifier': '*',
      },
      'SMCProcessor': {
        'specifier': '*',
      },
    }
  }

  # This should not raise an AssertionError
  validate_dependencies(lockfile, build_config)


def test_validate_dependencies_wildcard_missing_children():
  """Test that lock --check fails when wildcard children are missing."""
  lockfile = {
    'dependencies': {
      'Kexts': {
        'VirtualSMC': {
          'name': 'VirtualSMC',
          'specifier': 'latest',
          'version': '1.3.2',
          'url': 'https://github.com/acidanthera/VirtualSMC/releases/download/1.3.2/VirtualSMC-1.3.2-RELEASE.zip',
          'build': 'RELEASE',
          'kind': 'Kext',
          'resolution': 'acidanthera/VirtualSMC@github:1.3.2#checksum=abc123',
        },
        # Missing SMCBatteryManager, SMCLightSensor, SMCProcessor
      }
    }
  }

  build_config = {
    'Kexts': {
      'VirtualSMC': {
        'specifier': 'latest',
      },
      'SMCBatteryManager': {
        'specifier': '*',
      },
      'SMCLightSensor': {
        'specifier': '*',
      },
      'SMCProcessor': {
        'specifier': '*',
      },
    }
  }

  # This should raise AssertionError for missing entries
  with pytest.raises(AssertionError, match='missing new build configuration entries'):
    validate_dependencies(lockfile, build_config)


def test_validate_dependencies_wildcard_extra_children():
  """Test that lock --check fails when lockfile has extra wildcard children."""
  lockfile = {
    'dependencies': {
      'Kexts': {
        'VirtualSMC': {
          'name': 'VirtualSMC',
          'specifier': 'latest',
          'version': '1.3.2',
          'url': 'https://github.com/acidanthera/VirtualSMC/releases/download/1.3.2/VirtualSMC-1.3.2-RELEASE.zip',
          'build': 'RELEASE',
          'kind': 'Kext',
          'resolution': 'acidanthera/VirtualSMC@github:1.3.2#checksum=abc123',
        },
        'SMCBatteryManager': {
          'name': 'SMCBatteryManager',
          'specifier': '*',
          'version': '1.3.2',
          'url': 'https://github.com/acidanthera/VirtualSMC/releases/download/1.3.2/VirtualSMC-1.3.2-RELEASE.zip',
          'build': 'RELEASE',
          'kind': 'Kext',
          'resolution': 'acidanthera/VirtualSMC@github:1.3.2#checksum=abc123',
          '_wildcard_parent': 'VirtualSMC',
        },
        'ExtraChild': {
          'name': 'ExtraChild',
          'specifier': '*',
          'version': '1.3.2',
          'url': 'https://github.com/acidanthera/VirtualSMC/releases/download/1.3.2/VirtualSMC-1.3.2-RELEASE.zip',
          'build': 'RELEASE',
          'kind': 'Kext',
          'resolution': 'acidanthera/VirtualSMC@github:1.3.2#checksum=abc123',
          '_wildcard_parent': 'VirtualSMC',
        },
      }
    }
  }

  build_config = {
    'Kexts': {
      'VirtualSMC': {
        'specifier': 'latest',
      },
      'SMCBatteryManager': {
        'specifier': '*',
      },
      # Missing SMCLightSensor, SMCProcessor
    }
  }

  # This should raise AssertionError for outdated entries
  with pytest.raises(AssertionError, match='outdated build configuration entries'):
    validate_dependencies(lockfile, build_config)


@pytest.mark.parametrize('update', [False, True])
@pytest.mark.parametrize('default,override', [
  ('RELEASE', None), ('DEBUG', 'RELEASE'),
])
def test_build_selection_preserves_dependency_version(
    monkeypatch, default, override, update):
  from unittest.mock import Mock
  from ocebuild.sources.resolver import GitHubResolver, DortaniaResolver

  release = 'https://github.com/owner/Example/releases'
  locked = {
    'build': 'DEBUG', 'version': '1.0.0',
    'url': release + '/download/v1.0.0/Example-DEBUG.zip',
    'resolution': 'owner/Example@github:1.0.0#commit=abc123',
    'specifier': 'owner/Example@github:latest',
    'revision': '{ SHA1: abc123 }', 'kind': 'Kext',
  }
  fetch = Mock(return_value={'tag_name': 'v1.0.0', 'assets': [{
    'name': 'Example-RELEASE.zip',
    'browser_download_url': release + '/download/v1.0.0/Example-RELEASE.zip',
  }]})
  monkeypatch.setattr('ocebuild.sources.resolver.github_release_catalog', fetch)
  monkeypatch.setattr(DortaniaResolver, 'has_build', lambda name: False)

  def resolve(resolver, build=None):
    resolver.commit = 'abc123'
    return resolver.extract_asset(
      resolver, 'Example', release + '/tag/v1.0.0', build)

  monkeypatch.setattr(GitHubResolver, 'resolve', resolve)
  dependency = {'specifier': 'owner/Example=latest'}
  if override:
    dependency['build'] = override
  config = {
    'OpenCorePkg': {'OpenCore': {'specifier': '*', 'build': default}},
    'Kexts': {'Example': dependency},
  }
  lockfile = {'dependencies': {'Kexts': {'Example': locked}}}
  entries = resolve_specifiers(config, lockfile, update=update)
  resolved = next(entry for entry in entries if entry['name'] == 'Example')

  assert resolved['build'] == 'RELEASE'
  assert resolved['url'].endswith('Example-RELEASE.zip')
  for key in ('version', 'revision', 'resolution', 'specifier'):
    assert resolved[key] == locked[key]
  fetch.assert_called_once_with(release + '/tag/v1.0.0')
