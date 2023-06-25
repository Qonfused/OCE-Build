## @file
# Methods for handling and extracting remote archives.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

from cgi import parse_header
from contextlib import contextmanager
from pathlib import Path
from shutil import copytree, rmtree, unpack_archive
from tempfile import mkdtemp, NamedTemporaryFile
from urllib.request import Request

from typing import Generator, Literal, Union

from filesystem.posix import move, glob
from parsers.plist import parse_plist
from versioning.constants import OPENCORE_BINARY_DATA_URL
from versioning.sources import request


@contextmanager
def extract_archive(url: Union[str, Request],
                    persist: bool=False
                    ) -> Generator[Path, str, None]:
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
    with request(url) as response:
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

@contextmanager
def extract_opencore_archive(url: str,
                             target: Literal['IA32', 'X64']='X64',
                             persist: bool=False
                             ) -> Generator[Path, any, None]:
  """"""
  tmp_dir = mkdtemp()
  try:
    # Extract specified OpenCore package
    with extract_archive(url) as pkg:
      # Extract EFI binaries and tree structure
      EFI_DIR = move(glob(pkg, pattern=f'**/{target}/EFI', first=True), tmp_dir)
      # Extract ACPI samples
      acpi_samples = glob(pkg, pattern='**/Docs/AcpiSamples/Binaries/*.aml')
      for file in acpi_samples: move(file, EFI_DIR.joinpath('OC', 'ACPI'))
      # Extract sample config.plist
      sample_plist = glob(pkg, pattern='**/Docs/Sample.plist', first=True)
      move(sample_plist, EFI_DIR.joinpath('OC'), name='config.plist')
      
      # Extract documentation files
      DOCS_DIR = EFI_DIR.joinpath('..', 'Docs')
      changelog_doc = glob(pkg, pattern='**/Docs/Changelog.md', first=True)
      move(changelog_doc, DOCS_DIR)
      config_doc = glob(pkg, pattern='**/Docs/Configuration.pdf', first=True)
      move(config_doc, DOCS_DIR)

      # Extract bundled utilities
      UTILITIES_DIR = EFI_DIR.joinpath('..', 'Utilities')
      for dir in glob(pkg, pattern='**/Utilities/*/'): move(dir, UTILITIES_DIR)

    # Clone latest additional OpenCore binaries not shipped in the main package
    with extract_archive(OPENCORE_BINARY_DATA_URL) as pkg:
      for dir in glob(EFI_DIR, pattern='**/OC/*/'):
        extract = glob(pkg, pattern=f'**/{dir.name}/', first=True)
        if extract and extract.exists():
          copytree(extract, dir, dirs_exist_ok=True)
    
    # Yield the temporary directory.
    yield Path(tmp_dir)
  finally:
    # Cleanup after context exits
    if not persist: rmtree(tmp_dir)
