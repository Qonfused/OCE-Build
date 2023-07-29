## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

import pytest
from packaging import version as vpkg

from .semver import *


# from ocebuild.pipeline.kexts_test import __virtualsmc_archive


def test_get_version_str():
  # Validate semver strings
  version = '1.0.0'
  expected = version
  for symbol in reversed([*SEMVER_SYMBOLS, *COMPARISON_SYMBOLS]):
    assert get_version_str(f'{symbol}{version}') == expected
  # Validate fallthrough cases
  assert get_version_str(version) == expected
  assert get_version_str('latest') == 'latest'
  assert get_version_str('oldest') == 'oldest'
  assert get_version_str('foo') == 'foo'

def test_get_version():
  # Validate semver strings
  version = '1.0.0'
  expected = vpkg.Version(version)
  for symbol in reversed([*SEMVER_SYMBOLS, *COMPARISON_SYMBOLS]):
    assert get_version(f'{symbol}{version}') == expected
  # Validate fallthrough cases
  assert get_version(version) == expected
  assert not get_version('latest')
  assert not get_version('oldest')
  assert not get_version('foo')

def test_compare_version():
  version_a = '1.0.0'
  version_b = '2.0.0'

  # Test comparisons
  assert not compare_version(version_a, version_b, '>')
  assert     compare_version(version_b, version_a, '>')

  assert     compare_version(version_a, version_b, '<')
  assert not compare_version(version_b, version_a, '<')

  assert not compare_version(version_a, version_b, '>=') # >
  assert     compare_version(version_a, version_a, '>=') # ==
  assert     compare_version(version_b, version_a, '>=') # >
  assert     compare_version(version_b, version_b, '>=') # ==

  assert     compare_version(version_a, version_b, '<=') # <
  assert     compare_version(version_a, version_a, '<=') # ==
  assert not compare_version(version_b, version_a, '<=') # <
  assert     compare_version(version_b, version_b, '<=') # ==

  assert not compare_version(version_a, version_b, '==')
  assert     compare_version(version_a, version_a, '==')
  assert not compare_version(version_b, version_a, '==')
  assert     compare_version(version_b, version_b, '==')

  assert     compare_version(version_a, version_b, '!=')
  assert not compare_version(version_a, version_a, '!=')
  assert     compare_version(version_b, version_a, '!=')
  assert not compare_version(version_b, version_b, '!=')

  assert not compare_version(version_a, version_b, '~')

def test_resolve_version_specifier():
  versions = ['1.2.2', '1.2.3', '1.2.4', '1.3.0', '1.3.1', '2.0.0']

  # Up to next minor
  # e.g. '~1.2.3' -> '>=1.2.3,<1.3.0'
  assert resolve_version_specifier(versions, '~1.2.2')  == '1.2.4'

  # Up to next major
  # e.g. '^1.2.3' -> '>=1.2.3,<2.0.0'
  assert resolve_version_specifier(versions, '^1.2.2')  == '1.3.1'

  # Exact match
  # e.g. '1.2.3' -> '==1.2.3'
  assert resolve_version_specifier(versions, '1.2.3')   == '1.2.3'

  # Direct comparisons
  assert resolve_version_specifier(versions, '>1.2.3')  == '2.0.0'
  assert resolve_version_specifier(versions, '<1.2.3')  == '1.2.2'
  assert resolve_version_specifier(versions, '>=1.2.3') == '2.0.0'
  assert resolve_version_specifier(versions, '<=1.2.3') == '1.2.3'
  assert resolve_version_specifier(versions, '==1.2.3') == '1.2.3'
  assert resolve_version_specifier(versions, '!=1.2.3') == '2.0.0'

  # Named specifiers
  assert resolve_version_specifier(versions, 'latest') == '2.0.0'
  assert resolve_version_specifier(versions, 'oldest') == '1.2.2'

  # Fallthrough
  assert resolve_version_specifier(versions, 'foo') is None
  assert resolve_version_specifier([], '1.2.3') is None

def test_get_minimum_version(): pass # Not implemented

# def test_sort_dependencies(__virtualsmc_archive):
#   # Verify kext dependencies are sorted correctly
#   kext_order = [('as.vit9696.Lilu', '^1.2.0'),
#                 ('as.vit9696.VirtualSMC', '^1.0.0'),
#                 ('as.lvs1974.SMCDellSensors', None),
#                 ('ru.joedm.SMCSuperIO', None),
#                 ('ru.usrsse2.SMCBatteryManager', None),
#                 ('as.vit9696.SMCProcessor', None),
#                 ('ru.usrsse2.SMCLightSensor', None)]
#   assert list(sort_dependencies(__virtualsmc_archive))[:2] == kext_order[:2]
