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
