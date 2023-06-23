## @file
# Methods for handling and extracting remote archives.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

from cgi import parse_header
from contextlib import contextmanager
from pathlib import Path
from ssl import _create_unverified_context as skip_ssl_verify
from shutil import rmtree, unpack_archive
from tempfile import mkdtemp, NamedTemporaryFile
from urllib.request import urlopen, Request

from typing import Generator

from parsers.plist import parse_plist


@contextmanager
def extract_archive(url: str | Request,
                    persist: bool=False) -> Generator[Path, str, None]:
  """Extracts a file from a URL and yields a temporary extraction directory.

  Args:
    url: URL of the archive file.
    persist: Flag to disable cleanup of the temporary directory.

  Yields:
    tmp_dir (str): Path to the temporary directory.

  Example:
    >>> with extract_archive('https://example.com/foo.zip') as tmp_dir:
    print(tmp_dir)
    # -> "/tmp/xxxxxx"
  """
  tmp_dir = mkdtemp()
  try:
    with urlopen(url, context=skip_ssl_verify()) as response:
      # Extract filename from request headers.
      _, params = parse_header(response.headers.get('Content-Disposition', ''))
      filename = params['filename']
      extension = "".join(Path(filename).suffixes)
      # Write archive to a temporary file.
      with NamedTemporaryFile(suffix=extension) as tmp_file:
        tmp_file.write(response.read())
        tmp_file.seek(0)
        # Extract the zip file to the temporary directory.
        unpack_archive(tmp_file.name, tmp_dir)
    # Yield the temporary directory.
    yield Path(tmp_dir)
  finally:
    # Cleanup after context exits
    if not persist: rmtree(tmp_dir)

@contextmanager
def extract_kexts(url: str,
                  persist: bool=False) -> Generator[dict, any, None]:
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
    #     '__path': Path('/tmp/foo/Foo.kext'),
    #     '__url': 'https://example.com/foo.zip',
    #     'identifier': 'com.example.foo',
    #     'version': '1.0.0',
    #     'extract': './Foo.kext',
    #     'dependencies': {
    #       'com.example.bar': '1.0.0'
    #     }
    #   }
    # }
  """
  kexts = dict()
  try:
    with extract_archive(url, persist=True) as pkg:
      for plist_path in pkg.glob('**/*.kext/Contents/Info.plist'):
        kext_path = Path(plist_path).parents[1]
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
