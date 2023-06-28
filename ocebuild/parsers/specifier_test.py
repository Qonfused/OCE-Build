## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

import pytest

from parsers.specifier import *
from parsers.yaml import parse_yaml


def test_parse_specifier():
  build_file = parse_yaml(open('example/build.yml', 'r', encoding='UTF-8'))
  # Enumerate kext specifiers
  for kext, entry in build_file['Kexts'].items():
    assert parse_specifier(kext, entry).resolve()
