## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

import pytest

from .binary import *
from .github import github_archive_url

from ocebuild.filesystem.archives import extract_archive


def test_get_binary_ext():
  ext = get_binary_ext()
  assert f'iasl{ext}' in ('iasl', 'iasl.exe', 'iasl.linux')

def test_wrap_binary():
  iasl_url = github_archive_url(repository='Qonfused/iASL')
  with extract_archive(iasl_url) as tmpdir:
    binary = f'iasl{get_binary_ext()}'
    stdout = wrap_binary(args=['-v'],
                         binary_path=tmpdir.joinpath('iASL-main', binary))
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
    else:
      raise AssertionError(f'Unknown binary format: {binary}')
