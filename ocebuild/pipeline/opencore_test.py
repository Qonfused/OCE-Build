## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

import pytest

from ocebuild.errors.validation import validate_path_tree
from ocebuild.pipeline.opencore import *
from ocebuild.sources.github import github_tag_names
from ocebuild.versioning.semver import get_version


def test_extract_opencore_archive():
  latest_tag = sorted(github_tag_names('acidanthera/OpenCorePkg'),
                       key=lambda t: get_version(t))[-1]
  url = f'https://github.com/acidanthera/OpenCorePkg/releases/download/{latest_tag}/OpenCore-{latest_tag}-DEBUG.zip'
  
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
