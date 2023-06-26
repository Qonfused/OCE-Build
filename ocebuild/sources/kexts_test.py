## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

import pytest

from parsers.yaml import parse_yaml
from sources.kexts import *

from pprint import pprint


def test_get_kext_release(): pass
  # # resolution = '@OpenIntelWireless/itlwm@github:v2.0.0'
  # # resolution = '@acidanthera/RestrictEvents@github#branch=force-vmm-install,commit=e5c52564f5bca1aebbd916f2753f5a58809703a8'
  # filepath = 'example/build.yml'
  # # filepath = '/Volumes/RAID-1/GitHub/ASUS-ZenBook-Duo-14-UX481-Hackintosh/src/build.lock'
  # with open(filepath, 'r', encoding='UTF-8') as file:
  #   cfg = parse_yaml(file)
  #   with open("example/output.log", "w") as output:
  #     pprint(cfg, indent=1, stream=output)
