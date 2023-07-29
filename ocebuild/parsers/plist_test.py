## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

import pytest

from .dict import nested_get
from .plist import *

from ocebuild.filesystem.archives import extract_archive
from ocebuild.sources import request
from ocebuild.sources.binary import get_binary_ext, wrap_binary
from ocebuild.sources.github import github_file_url, github_tag_names
from ocebuild.versioning.semver import get_version


def test_parse_plist():
  url = github_file_url('acidanthera/OpenCorePkg',
                        path='Docs/Sample.plist',
                        branch='master',
                        tag='0.9.3',
                        raw=True)
  with request(url).text(encoding='utf-8') as file:
    sample_plist = parse_plist(file)
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
    # Deep compare
    assert nested_get(sample_plist, ['DeviceProperties']) == {
      'Add': {
        'PciRoot(0x0)/Pci(0x1b,0x0)': {
          'layout-id': b'\x01\x00\x00\x00'
        }
      },
      'Delete': {}
    }

def test_write_plist():
  latest_tag = sorted(github_tag_names('acidanthera/OpenCorePkg'),
                       key=lambda t: get_version(t))[-1]
  url = f'https://github.com/acidanthera/OpenCorePkg/releases/download/{latest_tag}/OpenCore-{latest_tag}-DEBUG.zip'
  with extract_archive(url) as opencore_dir:
    # Parse sample config.plist to dict
    config_plist_filepath = opencore_dir.joinpath('Docs', 'Sample.plist')
    with open(config_plist_filepath, 'r', encoding='utf-8') as file:
      sample_plist = parse_plist(file)
    # Write parsed config.plist as plist
    output_plist_filepath = opencore_dir.joinpath('Docs', 'Sample.plist')
    with open(output_plist_filepath, 'w') as f:
      lines = write_plist(sample_plist)
      f.writelines(lines)
    # Validate output with ocvalidate binary
    ocvalidate_binary = f'ocvalidate{get_binary_ext()}'
    stdout = wrap_binary(args=[output_plist_filepath],
                         binary_path=opencore_dir.joinpath('Utilities', 'ocvalidate', ocvalidate_binary))
    assert 'No issues found.' in stdout
