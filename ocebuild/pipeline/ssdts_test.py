## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

import pytest

from ocebuild.pipeline.ssdts import *


def test_sort_ssdt_symbols():
  mock_path = 'ci/mock'
  filepaths = list(map(lambda s: f'{mock_path}/ACPI/{s}.dsl', [
    'SSDT-A',
    'SSDT-B'
  ]))
  output = sort_ssdt_symbols(filepaths)
  assert output['DSDT'] == ['SB.PCI0', 'SB.PCI0.FIZ']
  assert output['SSDT-A'] == ['QUX', 'SB.BAZ', 'SB.PCI0.QUUX']
  assert output['SSDT-B'] == ['BUUF', 'BUUX', 'FUUB', 'SB.BAR', 'SB.FOO', 'SB.FOO.XUUQ']
