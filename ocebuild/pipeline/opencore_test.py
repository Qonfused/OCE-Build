## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

import pytest

from errors.validation import validate_path_tree
from pipeline.opencore import *


def test_extract_opencore_archive():
  url = 'https://github.com/acidanthera/OpenCorePkg/releases/download/0.9.3/OpenCore-0.9.3-DEBUG.zip'
  
  with extract_opencore_archive(url) as pkg:
    # Verify tree structure exists
    efi_tree = {
      'Docs': {
        'Changelog.md': 'f',
        'Configuration.pdf': 'f'
      },
      'EFI': {
        'BOOT': {
          'BOOTx64.efi': 'f'
        },
        'OC': {
          'ACPI': '*',
          'Drivers': '*',
          'Kexts': 'd',
          'Resources': {
            'Audio': '*',
            'Font': '*',
            'Image': {
              'Acidanthera': { 
                'Chardonnay': '*',
                'GoldenGate': '*',
                'Syrah': '*'
              }
            },
            'Label': '*',
          },
          'Tools': '*',
          'config.plist': 'f',
          'OpenCore.efi': 'f'
        }
      },
      'Utilities': {
        'macrecovery': {
          'boards.json': 'f',
          'macrecovery.py': 'f'
        },
        'macserial': {
          'macserial': 'f',
          'macserial.exe': 'f',
          'macserial.linux': 'f'
        },
        'ocvalidate': {
          'ocvalidate': 'f',
          'ocvalidate.exe': 'f',
          'ocvalidate.linux': 'f'
        }
      }
    }
    assert validate_path_tree(pkg, efi_tree)
