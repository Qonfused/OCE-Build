## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Methods for retrieving and handling OpenCore packages."""

from contextlib import contextmanager
from shutil import copytree, rmtree
from tempfile import mkdtemp

from typing import Generator, Literal

from ocebuild.filesystem.archives import extract_archive
from ocebuild.filesystem.posix import glob, move
from ocebuild.sources.github import github_archive_url
from ocebuild.sources.resolver import PathResolver


OPENCORE_BINARY_DATA_URL = github_archive_url('acidanthera/OcBinaryData',
                                              branch='master')

@contextmanager
def extract_opencore_archive(url: str,
                             target: Literal['IA32', 'X64']='X64',
                             persist: bool=False
                             ) -> Generator[PathResolver, any, None]:
  """Extracts the contents of an OpenCore archive and yields a temporary directory.
  
  Args:
    url: The URL of the OpenCore archive to extract.
    target: The target EFI architecture to extract. Defaults to 'X64'.
    persist: Whether to persist the temporary directory. Defaults to False.
  
  Yields:
    A temporary directory containing the extracted contents.
  """
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
    yield PathResolver(tmp_dir)
  finally:
    # Cleanup after context exits
    if not persist: rmtree(tmp_dir)


__all__ = [
  # Constants (1)
  "OPENCORE_BINARY_DATA_URL",
  # Functions (1)
  "extract_opencore_archive"
]
