## @file
# Methods for retrieving and handling Kext packages.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

from contextlib import contextmanager
from shutil import rmtree

from typing import Generator, Literal, Union

from ocebuild.filesystem.archives import extract_archive
from ocebuild.parsers.plist import parse_plist
from ocebuild.sources.resolver import GitHubResolver, DortaniaResolver, PathResolver


@contextmanager
def extract_kext_archive(url: str,
                         persist: bool=False
                         ) -> Generator[dict, any, None]:
  """Extracts Kexts from a URL and yields a temporary extraction dictionary.

  Args:
    url: URL of the archive file.
    persist: Flag to disable cleanup of the temporary directory.

  Yields:
    kexts (dict): Dictionary of extracted kexts.

  Example:
    >>> with extract_kexts('https://example.com/foo.zip') as kexts:
    ...   print(kexts)
    # -> {
    #   'Foo': {
    #     '__extract': './Foo.kext'
    #     '__path': Path('/tmp/foo/Foo.kext'),
    #     '__url': 'https://example.com/foo.zip',
    #     'identifier': 'com.example.foo',
    #     'version': '1.0.0',
    #     'dependencies': {
    #       'com.example.bar': '1.0.0'
    #     }
    #   },
    #   'Bar': { ... }
    # }
  """
  kexts = dict()
  try:
    with extract_archive(url, persist=True) as pkg:
      for plist_path in pkg.glob('**/*.kext/Contents/Info.plist'):
        kext_path = PathResolver(plist_path).parents[1].as_posix()
        extract_path = f'.{str(kext_path)[len(str(pkg)):]}'
        with open(plist_path, 'r', encoding='UTF-8') as file:
          # Build plist dictionary from filestream
          plist = parse_plist(file)
          # Extract Kext bundle properties
          name = plist['CFBundleName'][1]
          identifier = plist['CFBundleIdentifier'][1]
          version = plist['CFBundleVersion'][1]
          executable = plist['CFBundleExecutable'][1]
          libraries = { k:v[1] for k,v in plist['OSBundleLibraries'].items()
                            # Ignore self-dependencies
                        if (not k == identifier and
                            # Ignore Apple-provided libraries
                            not k.startswith('com.apple.')) }
          # Cleanup
          del plist
        # Update kext dictionary
        kexts[name] = {
          "__extract": extract_path,
          "__path": kext_path,
          "__url": url,
          "identifier": identifier,
          "version": version,
          "executable": executable,
          "dependencies": libraries
        }
    # Yield the kexts dictionary.
    yield kexts
  finally:
    # Cleanup after context exits
    if not persist: rmtree(pkg)
