## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Methods for retrieving and handling OpenCore packages."""

from contextlib import contextmanager
from shutil import copy, copytree, rmtree
from tempfile import mkdtemp

from typing import Generator, Iterator, List, Literal, Optional, Union

from ocebuild.filesystem.archives import extract_archive
from ocebuild.filesystem.posix import glob, move, remove
from ocebuild.sources.github import github_archive_url
from ocebuild.sources.resolver import PathResolver


OPENCORE_BINARY_DATA_URL = github_archive_url('acidanthera/OcBinaryData',
                                              branch='master')

def _iterate_entries(opencore_pkg: PathResolver,
                     OC_DIR: PathResolver
                     ) -> Generator[PathResolver, any, None]:
  """Iterate over the entries in the build configuration."""
  for category in map(lambda p: p.name, OC_DIR.iterdir()):
    if category not in ('ACPI', 'Drivers', 'Kexts', 'Tools'): continue
    for path in map(lambda p: p.relative_to(opencore_pkg).as_posix(),
                    OC_DIR.joinpath(category).iterdir()):
      yield path


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
      
      # Extract documentation files
      DOCS_DIR = EFI_DIR.joinpath('..', 'Docs')
      changelog_doc = glob(pkg, pattern='**/Docs/Changelog.md', first=True)
      move(changelog_doc, DOCS_DIR)
      config_doc = glob(pkg, pattern='**/Docs/Configuration.pdf', first=True)
      move(config_doc, DOCS_DIR)
      diff_doc = glob(pkg, pattern='**/Docs/Differences.pdf', first=True)
      move(diff_doc, DOCS_DIR)

      # Extract sample config.plist
      sample_plist = glob(pkg, pattern='**/Docs/Sample.plist', first=True)
      copy(sample_plist, DOCS_DIR)
      move(sample_plist, EFI_DIR.joinpath('OC'), name='config.plist')

      # Extract ACPI samples
      acpi_samples = glob(pkg, pattern='**/Docs/AcpiSamples/Binaries/*.aml')
      for file in acpi_samples: move(file, EFI_DIR.joinpath('OC', 'ACPI'))

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

def extract_opencore_directory(resolvers: dict,
                               lockfile: dict,
                               target: str,
                               out_dir: Union[str, PathResolver],
                               *args,
                               __wrapper: Optional[Iterator]=None,
                               **kwargs
                               ) -> Union[PathResolver, None]:
  """Extracts the OpenCore pacakge from the build OpenCore configuration.
  
  Args:
    resolvers: The build configuration resolvers.
    lockfile: The build configuration lockfile.
    target: The target EFI architecture to extract.
    out_dir: The output directory to extract the OpenCore package to.
    *args: Additional arguments to pass to the optional iterator wrapper.
    __wrapper: A wrapper function to apply to the iterator. (Optional)
    **kwargs: Additional keyword arguments to pass to the optional iterator wrapper.

  Returns:
    A PathResolver to the extracted OpenCore directory.
  """
  url = resolvers['OpenCore']['url']
  #TODO: Add OpenCore to the lockfile
  del resolvers['OpenCore']

  with extract_opencore_archive(url, target=target) as opencore_pkg:
    OC_DIR = opencore_pkg.joinpath('EFI', 'OC')
    
    # Handle interactive mode for iterator
    iterator = set(_iterate_entries(opencore_pkg, OC_DIR))
    num_entries = len(iterator)
    if __wrapper is not None: iterator = __wrapper(iterator, *args, **kwargs)
    
    # Iterate over the entries in the extracted OpenCore package
    bundled = set(v['__filepath'] for v in resolvers.values()
                  if v['specifier'] == '*')
    for idx, path in enumerate(iterator):
      # Include only binaries that are specified as bundled in the build config
      if path not in bundled:
        remove(opencore_pkg.joinpath(path))
      else:
        #TODO: Add entry under OpenCore's `bundled` property
        bundled.discard(path)
        del resolvers[PathResolver(path).stem]
      # Copy the remaining files to the output directory
      if idx + 1 == num_entries: # This stalls the iterator until completion
        copytree(opencore_pkg, out_dir, dirs_exist_ok=True)
        return PathResolver(out_dir, OC_DIR.relative_to(opencore_pkg))


__all__ = [
  # Constants (1)
  "OPENCORE_BINARY_DATA_URL",
  # Functions (2)
  "extract_opencore_archive",
  "extract_opencore_directory"
]
