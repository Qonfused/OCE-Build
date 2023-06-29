## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

import pytest

from pipeline.kexts import *


@pytest.fixture
def __virtualsmc_archive():
  dependencies = dict()
  url = 'https://github.com/acidanthera/VirtualSMC/releases/download/1.3.2/VirtualSMC-1.3.2-DEBUG.zip'
  with extract_kext_archive(url) as kexts:
    for kext in kexts.values():
      key = kext['identifier']
      entries = kext['dependencies']
      dependencies[key] = [(k, entries[k]) for k in set(entries.keys())]
  return dependencies

def test_extract_kext_archive(__virtualsmc_archive):
  # Verify kext dependencies are extracted correctly
  assert sorted(__virtualsmc_archive['as.vit9696.VirtualSMC']) == \
    [('as.vit9696.Lilu', '1.2.0')]
  assert sorted(__virtualsmc_archive['ru.usrsse2.SMCBatteryManager']) == \
    [('as.vit9696.Lilu', '1.2.0'),
     ('as.vit9696.VirtualSMC', '1.0.0')]
  assert sorted(__virtualsmc_archive['as.lvs1974.SMCDellSensors']) == \
    [('as.vit9696.Lilu', '1.2.0'),
     ('as.vit9696.VirtualSMC', '1.0.0')]
  assert sorted(__virtualsmc_archive['as.vit9696.SMCProcessor']) == \
    [('as.vit9696.Lilu', '1.2.0'),
     ('as.vit9696.VirtualSMC', '1.0.0')]
  assert sorted(__virtualsmc_archive['ru.usrsse2.SMCLightSensor']) == \
    [('as.vit9696.Lilu', '1.2.0'),
     ('as.vit9696.VirtualSMC', '1.0.0')]
  assert sorted(__virtualsmc_archive['ru.joedm.SMCSuperIO']) == \
    [('as.vit9696.Lilu', '1.2.0'),
     ('as.vit9696.VirtualSMC', '1.0.0')]
