## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

import pytest

from datetime import datetime, timezone

from parsers.plist import *


plist_dummy_types = [
  [('array',  []), []],
  [('data', 'AQ=='), ('data', '01')],
  [('date', '2020-01-01T00:00:00Z'), ('date', datetime(2020, 1, 1, 0, 0, tzinfo=timezone.utc))],
  [('dict', {}), {}],
  [('real', '1.0'), ('float', 1.0)],
  [('integer',  '1'), ('int', 1)],
  [('string', 'Foo'), ('string', 'Foo')],
  [('true', ''), ('bool', True)],
  [('false', ''), ('bool', False)],
]

def test_parse_serialized_types():
  for input, expected in plist_dummy_types:
    assert parse_serialized_types(*input) == expected
  
def test_write_serialized_types():
  pass
  # for (stype, svalue), input in plist_dummy_types:
  #   if len(input) == 1: input = (None, input)
  #   if stype == 'array':
  #     defaults = ('array', None)
  #     expected = [f'<array>', f'</array>']
  #     assert write_serialized_types(input, defaults) == expected
  #   else:
  #     expected = None
  #     if stype == 'bool':
  #       expected = [f'<{(stype := str(svalue).lower())}/>']
  #       assert write_serialized_types(input) == expected
  #     elif stype == 'dict':
  #       expected = [f'<dict>', f'</dict>']
  #       assert write_serialized_types(input) == expected
  #     else:
  #       expected = [f'<{stype}>', f'</{stype}>']
  #       assert write_serialized_types(input) == expected
  #     # Default entry schema
  #     if expected is None:
  #       expected = [f'<{stype}>{svalue}</{stype}>']
  #     assert write_serialized_types(input, defaults) == expected

def test_parse_plist():
  from sources._lib import request
  from sources.github import github_file_url

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

def test_write_plist(): pass # Not implemented
