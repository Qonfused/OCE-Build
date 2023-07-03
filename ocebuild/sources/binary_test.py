## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

import pytest

from ocebuild.sources.binary import *
from ocebuild.sources.resolver import PathResolver


def test_get_binary_ext():
  ext = get_binary_ext()
  assert PathResolver(f'scripts/lib/iasl/iasl{ext}').exists()

def test_wrap_binary():
  binary = f'iasl{get_binary_ext()}'
  stdout = wrap_binary(args=['-v'],
                       binary_path=f'scripts/lib/iasl/{binary}')
  if   binary == 'iasl':
    assert stdout.strip() == "\n".join([
      "Intel ACPI Component Architecture",
      "ASL+ Optimizing Compiler/Disassembler version 20200925",
      "Copyright (c) 2000 - 2020 Intel Corporation",
    ])
  elif binary == 'iasl.exe':
    assert stdout.strip() == "\n".join([
      "Intel ACPI Component Architecture",
      "ASL+ Optimizing Compiler/Disassembler version 20230331",
      "Copyright (c) 2000 - 2023 Intel Corporation",
    ])
  elif binary == 'iasl.linux':
    assert stdout.strip() == "\n".join([
      "Intel ACPI Component Architecture",
      "ASL+ Optimizing Compiler/Disassembler version 20180105",
      "Copyright (c) 2000 - 2018 Intel Corporation",
    ])
