## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Methods for retrieving and handling Kext packages and binaries."""

from typing import Literal, Union

from ocebuild.parsers.plist import parse_plist
from ocebuild.sources.resolver import PathResolver


def parse_kext_plist(filepath: Union[str, PathResolver]) -> dict:
  """Parses the Info.plist of a Kext."""
  with open(filepath, 'r', encoding='UTF-8') as file:
    # Build plist dictionary from filestream
    plist = parse_plist(file)
  # Extract Kext bundle properties
  name = plist['CFBundleName']
  identifier = plist['CFBundleIdentifier']
  version = plist['CFBundleVersion']
  executable = plist['CFBundleExecutable']
  libraries = { k:v for k,v in plist['OSBundleLibraries'].items()
                    # Ignore self-dependencies
                if (not k == identifier and
                    # Ignore Apple-provided libraries
                    not k.startswith('com.apple.')) }
  return {
    "identifier": identifier,
    "version": version,
    "executable": executable,
    "dependencies": libraries
  }

def extract_kexts(directory: Union[str, PathResolver],
                  build: Literal['RELEASE', 'DEBUG']='RELEASE',
                  ) -> list:
  """Extracts the metadata of all Kexts in a directory."""
  kexts = {}
  for plist_path in directory.glob('**/*.kext/Contents/Info.plist'):
    kext_path = PathResolver(plist_path).parents[1].as_posix()
    extract_path = f'.{str(kext_path).split(directory.as_posix())[1]}'
    plist_props = parse_kext_plist(plist_path)
    # Update kext dictionary
    kexts[plist_props['name']] = {
      "__extract": extract_path,
      "__path": kext_path,
      **plist_props
    }
  # Filter build targets if provided in extract path
  if any(build.lower() in e['__extract'].lower() for e in kexts.values()):
    kexts = { k:v for k,v in kexts.items()
              if build.lower() in v['__extract'].lower() }

  return kexts


__all__ = [
  # Functions (2)
  "parse_kext_plist",
  "extract_kexts"
]
