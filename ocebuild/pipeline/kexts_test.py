## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

import plistlib

import pytest

from .kexts import *


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

# def test_extract_kext_archive(__virtualsmc_archive):
#   # Verify kext dependencies are extracted correctly
#   assert sorted(__virtualsmc_archive['as.vit9696.VirtualSMC']) == \
#     [('as.vit9696.Lilu', '1.2.0')]
#   assert sorted(__virtualsmc_archive['ru.usrsse2.SMCBatteryManager']) == \
#     [('as.vit9696.Lilu', '1.2.0'),
#      ('as.vit9696.VirtualSMC', '1.0.0')]
#   assert sorted(__virtualsmc_archive['as.lvs1974.SMCDellSensors']) == \
#     [('as.vit9696.Lilu', '1.2.0'),
#      ('as.vit9696.VirtualSMC', '1.0.0')]
#   assert sorted(__virtualsmc_archive['as.vit9696.SMCProcessor']) == \
#     [('as.vit9696.Lilu', '1.2.0'),
#      ('as.vit9696.VirtualSMC', '1.0.0')]
#   assert sorted(__virtualsmc_archive['ru.usrsse2.SMCLightSensor']) == \
#     [('as.vit9696.Lilu', '1.2.0'),
#      ('as.vit9696.VirtualSMC', '1.0.0')]
#   assert sorted(__virtualsmc_archive['ru.joedm.SMCSuperIO']) == \
#     [('as.vit9696.Lilu', '1.2.0'),
#      ('as.vit9696.VirtualSMC', '1.0.0')]

#   # Verify build targets are extracted correctly
#   url = 'https://github.com/Qonfused/OCE-Build/files/11971818/WhateverGreen-CI.zip'
#   with extract_kext_archive(url) as kexts:
#     # Verify only 1 kext is extracted
#     assert len(kexts) == 1 and 'WhateverGreen' in kexts
#     # Verify kext props are extracted
#     assert kexts['WhateverGreen']['__path'] == \
#       './WhateverGreen-1.6.6-DEBUG.zip/WhateverGreen.kext'
#     assert kexts['WhateverGreen']['__url'] == url
#     assert kexts['WhateverGreen']['version'] == '1.6.6'


def _bundle(root, name, identifier, dependencies=None, version='1.0.0'):
  bundle = root / name
  contents = bundle / 'Contents'
  contents.mkdir(parents=True, exist_ok=True)
  info = {
    'CFBundleName': bundle.stem,
    'CFBundleIdentifier': identifier,
    'CFBundleVersion': version,
    'OSBundleLibraries': dependencies or {},
  }
  (contents / 'Info.plist').write_bytes(plistlib.dumps(info))
  return bundle


def test_grouping_preserves_library_dependencies(tmp_path):
  parent = _bundle(tmp_path, 'DuoLink.kext', 'example.duolink', {
    'example.lilu': '1.0.0', 'example.services': '1.0.0',
  })
  plugins = parent / 'Contents/PlugIns'
  _bundle(plugins, 'Services.kext', 'example.services')
  _bundle(plugins, 'Touch.kext', 'example.touch', {
    'example.duolink': '1.0.0', 'example.external': '1.0.0',
  })
  lilu = _bundle(tmp_path, 'Lilu.kext', 'example.lilu')
  external = _bundle(tmp_path, 'Z.kext', 'example.external')

  entries = sort_kext_cfbundle([parent, lilu, external])
  ids = [entry['identifier'] for entry in entries]
  assert ids.index('example.lilu') < ids.index('example.duolink')
  assert ids.index('example.services') < ids.index('example.duolink')
  assert ids.index('example.duolink') < ids.index('example.touch')
  assert ids.index('example.external') < ids.index('example.touch')


def test_provider_versions_remain_newest_first(tmp_path):
  older = _bundle(tmp_path, 'Older.kext', 'example.library', version='1.0.0')
  support = _bundle(tmp_path, 'Support.kext', 'example.support')
  newer = _bundle(tmp_path, 'Newer.kext', 'example.library',
                  {'example.support': '1.0.0'}, version='2.0.0')
  consumer = _bundle(tmp_path, 'Consumer.kext', 'example.consumer',
                     {'example.library': '1.0.0'})

  entries = sort_kext_cfbundle([older, consumer, newer, support])
  assert [entry['name'] for entry in entries] == [
    'Support', 'Newer', 'Older', 'Consumer',
  ]


def test_valid_dependency_order_is_preserved(tmp_path):
  library = _bundle(tmp_path, 'A.kext', 'example.a')
  consumer = _bundle(tmp_path, 'B.kext', 'example.b', {'example.a': '1.0.0'})
  other = _bundle(tmp_path, 'Z.kext', 'example.z')

  entries = sort_kext_cfbundle([library, consumer, other])
  assert [entry['name'] for entry in entries] == ['A', 'B', 'Z']
