## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Methods for retrieving and handling Kext packages and binaries."""

from typing import Literal, Union

from ocebuild.parsers.dict import nested_get
from ocebuild.parsers.plist import parse_plist
from ocebuild.sources.resolver import PathResolver


def parse_kext_plist(filepath: Union[str, PathResolver]) -> dict:
  """Parses the Info.plist of a Kext."""
  with open(filepath, 'r', encoding='UTF-8') as file:
    # Build plist dictionary from filestream
    plist = parse_plist(file)
  # Extract Kext bundle properties
  name = nested_get(plist, ['CFBundleName'])
  identifier = nested_get(plist, ['CFBundleIdentifier'])
  version = nested_get(plist, ['CFBundleVersion'])
  executable = nested_get(plist, ['CFBundleExecutable'])
  libraries = nested_get(plist, ['OSBundleLibraries'], default={})
  dependencies = { k:v for k,v in libraries.items()
                       # Ignore self-dependencies
                   if (not k == identifier and
                       # Ignore Apple-provided libraries
                       not k.startswith('com.apple.')) }
  return {
    "name": name,
    "identifier": identifier,
    "version": version,
    "executable": executable,
    "dependencies": dependencies
  }

def extract_kexts(directory: Union[str, PathResolver],
                  build: Literal['RELEASE', 'DEBUG']='RELEASE',
                  ) -> dict:
  """Extracts the metadata of all Kexts in a directory."""
  kexts = {}
  for plist_path in directory.glob('**/*.kext/**/Info.plist'):
    parent = str(plist_path).rsplit('.kext', maxsplit=1)[0]
    kext_path = PathResolver(f'{parent}.kext')
    extract_path = f'.{kext_path.as_posix().split(directory.as_posix())[1]}'
    # Update kext dictionary
    kexts[kext_path.stem] = {
      "__path": extract_path,
      "__extracted": kext_path,
    }

  # Filter build targets if provided in extract path
  if any(build.lower() in e['__path'].lower() for e in kexts.values()):
    kexts = { k:v for k,v in kexts.items()
              if build.lower() in v['__path'].lower() }

  return kexts


__all__ = [
  # Functions (2)
  "parse_kext_plist",
  "extract_kexts"
]
