## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

import pytest
from archives_test import __virtualsmc_archive

from versioning import *


def test_get_version_string(): pass # Not implemented

def test_get_version_parts(): pass # Not implemented

def test_compare_version(): pass # Not implemented

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
  assert resolve_version_specifier(versions, 'foo') == None

def test_get_minimum_version(): pass # Not implemented

def test_sort_dependencies(__virtualsmc_archive):
  # Verify kext dependencies are sorted correctly
  kext_order = [('as.vit9696.Lilu', '^1.2.0'),
                ('as.vit9696.VirtualSMC', '^1.0.0'),
                ('as.lvs1974.SMCDellSensors', None),
                ('ru.joedm.SMCSuperIO', None),
                ('ru.usrsse2.SMCBatteryManager', None),
                ('as.vit9696.SMCProcessor', None),
                ('ru.usrsse2.SMCLightSensor', None)]
  assert list(sort_dependencies(__virtualsmc_archive))[:2] == kext_order[:2]