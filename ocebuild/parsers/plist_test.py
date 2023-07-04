## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

import pytest

from datetime import datetime, timezone

from ocebuild.parsers.dict import nested_get
from ocebuild.parsers.plist import *
from ocebuild.pipeline.opencore import extract_opencore_archive
from ocebuild.sources._lib import request
from ocebuild.sources.binary import get_binary_ext, wrap_binary
from ocebuild.sources.github import github_tag_names, github_file_url
from ocebuild.versioning.semver import get_version


def test_parse_plist_types():
  assert parse_plist_types(*('array', [])) == \
    []
  assert parse_plist_types(*('data', 'AQ==')) == \
    ('data', '01')
  assert parse_plist_types('date', '2020-01-01T00:00:00Z') == \
    ('date', datetime(2020, 1, 1, 0, 0, tzinfo=timezone.utc))
  assert parse_plist_types('dict', {}) == \
    {}
  assert parse_plist_types('real', '1.0') == \
    ('float', 1.0)
  assert parse_plist_types('integer',  '1') == \
    ('int', 1)
  assert parse_plist_types('string', 'Foo') == \
    ('string', 'Foo')
  assert parse_plist_types('true', '') == \
    ('bool', True)
  assert parse_plist_types('false', '') == \
    ('bool', False)
  
def test_write_plist_types():
  mock_default = ('dict', '')
  assert write_plist_types([], defaults=('array', None)) == \
    ['<array>', '</array>']
  assert write_plist_types(('data', '01'), mock_default) == \
    ['<data>AQ==</data>']
  assert write_plist_types(('date', datetime(2020, 1, 1, 0, 0, tzinfo=timezone.utc)),
                                mock_default) == \
    ['<date>2020-01-01T00:00:00Z</date>']
  assert write_plist_types({}, defaults=('dict', None)) == \
    ['<dict>', '</dict>']
  assert write_plist_types(('float', 1.0), mock_default) == \
    ['<real>1.0</real>']
  assert write_plist_types(('int', 1), mock_default) == \
    ['<integer>1</integer>']
  assert write_plist_types(('string', 'Foo'), mock_default) == \
    ['<string>Foo</string>']
  assert write_plist_types(('bool', True), mock_default) == \
    ['<true/>']
  assert write_plist_types(('bool', False), mock_default) == \
    ['<false/>']

def test_parse_plist():
  url = github_file_url('acidanthera/OpenCorePkg',
                        path='Docs/Sample.plist',
                        branch='master',
                        tag='0.9.3',
                        raw=True)
  with request(url).text(encoding='utf-8') as file:
    sample_plist = parse_plist([l.rstrip() for l in file])
    # Validate schema
    entries = [
      # ACPI
      (list,  ['ACPI', 'Add']),
      (list,  ['ACPI', 'Delete']),
      (list,  ['ACPI', 'Patch']),
      (dict,  ['ACPI', 'Quirks']),
      # Booter
      (list,  ['Booter', 'MmioWhitelist']),
      (list,  ['Booter', 'Patch']),
      (dict,  ['Booter', 'Quirks']),
      # DeviceProperties
      (dict,  ['DeviceProperties', 'Add']),
      (dict,  ['DeviceProperties', 'Delete']),
      # Kernel
      (list,  ['Kernel', 'Add']),
      (list,  ['Kernel', 'Block']),
      (dict,  ['Kernel', 'Emulate']),
      (list,  ['Kernel', 'Force']),
      (list,  ['Kernel', 'Patch']),
      (dict,  ['Kernel', 'Quirks']),
      (dict,  ['Kernel', 'Scheme']),
      # Misc
      (list,  ['Misc', 'BlessOverride']),
      (dict,  ['Misc', 'Boot']),
      (dict,  ['Misc', 'Debug']),
      (list,  ['Misc', 'Entries']),
      (dict,  ['Misc', 'Security']),
      (dict,  ['Misc', 'Serial']),
      (list,  ['Misc', 'Tools']),
      # NVRAM
      (dict,  ['NVRAM', 'Add']),
      (dict,  ['NVRAM', 'Delete']),
      (bool,  ['NVRAM', 'LegacyOverwrite']),
      (dict,  ['NVRAM', 'LegacySchema']),
      (bool,  ['NVRAM', 'WriteFlash']),
      # PlatformInfo
      (bool,  ['PlatformInfo', 'Automatic']),
      (bool,  ['PlatformInfo', 'CustomMemory']),
      (dict,  ['PlatformInfo', 'Generic']),
      (bool,  ['PlatformInfo', 'UpdateDataHub']),
      (bool,  ['PlatformInfo', 'UpdateNVRAM']),
      (bool,  ['PlatformInfo', 'UpdateSMBIOS']),
      (str,   ['PlatformInfo', 'UpdateSMBIOSMode']),
      (bool,  ['PlatformInfo', 'UseRawUuidEncoding']),
      # UEFI
      (dict,  ['UEFI', 'APFS']),
      (dict,  ['UEFI', 'AppleInput']),
      (dict,  ['UEFI', 'Audio']),
      (bool,  ['UEFI', 'ConnectDrivers']),
      (list,  ['UEFI', 'Drivers']),
      (dict,  ['UEFI', 'Input']),
      (dict,  ['UEFI', 'Input']),
      (dict,  ['UEFI', 'Output']),
      (dict,  ['UEFI', 'ProtocolOverrides']),
      (dict,  ['UEFI', 'Quirks']),
      (list,  ['UEFI', 'ReservedMemory']),
    ]
    for _type, _tree in entries:
      assert (val := nested_get(sample_plist, _tree)) is not None
      if isinstance(val, tuple):
        _type, _val = val
        # Handle stringified types
        if (isinstance(_type, str)):
          if   _type == 'bool':     _type = bool
          elif _type == 'string':   _type = str
        assert isinstance(_val, _type)
      else:
        assert isinstance(val, _type)
    # Deep compare
    assert nested_get(sample_plist, ['DeviceProperties']) == {
      'Add': {
        'PciRoot(0x0)/Pci(0x1b,0x0)': {
          'layout-id': ('data', '01000000')
        }
      },
      'Delete': {}
    }

def test_write_plist():
  latest_tag = sorted(github_tag_names('acidanthera/OpenCorePkg'),
                       key=lambda t: get_version(t))[-1]
  url = f'https://github.com/acidanthera/OpenCorePkg/releases/download/{latest_tag}/OpenCore-{latest_tag}-DEBUG.zip'
  with extract_opencore_archive(url) as opencore_dir:
    # Parse sample config.plist to dict
    config_plist_filepath = opencore_dir.joinpath('EFI', 'OC', 'config.plist')
    with open(config_plist_filepath, 'r', encoding='utf-8') as file:
      sample_plist = parse_plist([l.rstrip() for l in file])
    # Write parsed config.plist as plist
    output_plist_filepath = opencore_dir.joinpath('EFI', 'OC', 'parsed.plist')
    with open(output_plist_filepath, 'w') as f:
      lines = write_plist(sample_plist)
      f.writelines("\n".join(lines))
    # Validate output with ocvalidate binary
    ocvalidate_binary = f'ocvalidate{get_binary_ext()}'
    stdout = wrap_binary(args=[output_plist_filepath],
                         binary_path=opencore_dir.joinpath('Utilities', 'ocvalidate', ocvalidate_binary))
    assert 'No issues found.' in stdout
