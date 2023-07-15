## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

import pytest

from .ssdts import *

from ci import EXAMPLE_PATH

from ocebuild.sources.resolver import PathResolver


def test_sort_ssdt_symbols():
  filepaths = list(map(lambda s: f'{EXAMPLE_PATH}/ACPI/{s}.dsl', [
    'SSDT-A',
    'SSDT-B'
  ]))
  output = sort_ssdt_symbols(filepaths)
  assert output['DSDT'] == ['SB.PCI0', 'SB.PCI0.FIZ']
  assert output['SSDT-A'] == ['QUX', 'SB.BAZ', 'SB.BAZ.HID', 'SB.PCI0.QUUX']
  assert output['SSDT-B'] == ['BUUF', 'BUUX', 'FUUB', 'SB.BAR', 'SB.FOO', 'SB.FOO.XUUQ']

def test_extract_iasl_binary():
  with extract_iasl_binary() as iasl_wrapper:
    iasl_wrapper(f'{EXAMPLE_PATH}/ACPI/SSDT-A.dsl')
    output_path = PathResolver(f'{EXAMPLE_PATH}/ACPI/SSDT-A.aml')
    assert output_path.exists()
  output_path.unlink()
