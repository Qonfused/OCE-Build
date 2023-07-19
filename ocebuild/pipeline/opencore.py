## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Methods for retrieving and handling OpenCore packages."""

from contextlib import contextmanager
from hashlib import sha256
from shutil import copy, copyfile, copytree, rmtree
from tempfile import mkdtemp, NamedTemporaryFile

from typing import Generator, Iterator, Literal, Optional, Union

from mmap import mmap, PROT_READ

from ocebuild.filesystem.archives import extract_archive
from ocebuild.filesystem.cache import UNPACK_DIR
from ocebuild.filesystem.posix import glob, move, remove
from ocebuild.parsers.dict import nested_get
from ocebuild.sources.binary import get_stream_digest
from ocebuild.sources.github import github_archive_url
from ocebuild.sources.resolver import PathResolver


OPENCORE_BINARY_DATA_URL = github_archive_url('acidanthera/OcBinaryData',
                                              branch='master')

def _iterate_entries(opencore_pkg: PathResolver,
                     opencore_dir: PathResolver
                     ) -> Generator[PathResolver, any, None]:
  """Iterate over the entries in the build configuration."""
  for category in map(lambda p: p.name, opencore_dir.iterdir()):
    if category not in ('ACPI', 'Drivers', 'Kexts', 'Tools'): continue
    for path in map(lambda p: p.relative_to(opencore_pkg).as_posix(),
                    opencore_dir.joinpath(category).iterdir()):
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
      for file in acpi_samples:
        move(file, EFI_DIR.joinpath('OC', 'ACPI'))

      # Extract bundled utilities
      UTILITIES_DIR = EFI_DIR.joinpath('..', 'Utilities')
      for dir_ in glob(pkg, pattern='**/Utilities/*/'):
        move(dir_, UTILITIES_DIR)

    # Clone latest additional OpenCore binaries not shipped in the main package
    with extract_archive(OPENCORE_BINARY_DATA_URL) as pkg:
      for dir_ in glob(EFI_DIR, pattern='**/OC/*/'):
        extract = glob(pkg, pattern=f'**/{dir_.name}/', first=True)
        if extract and extract.exists():
          copytree(extract, dir_, dirs_exist_ok=True)

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

  entry_path = ['dependencies', 'OpenCorePkg', 'OpenCore']
  url = nested_get(lockfile, [*entry_path, 'url'])
  if not url: url = nested_get(resolvers, [*entry_path[2:], 'url'])

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

def get_opencore_checksum(file_path: Union[str, PathResolver],
                          algorithm=sha256
                          ) -> str:
  """Computes the SHA256 checksum of the OpenCore binary.
  
  This will compute the checksum of the `OpenCore.efi` binary, substituting the
  embedded public key when using vaulting. Modifications are made to a copy of
  the file within a temporary directory, which is validated and deleted after
  computing the checksum.

  Args:
    file_path: The path to the OpenCore binary.
    algorithm: The hashlib algorithm to use. Defaults to SHA256.

  Raises:
    AssertionError: If the file checksum does not match the expected value.
    RuntimeError: If the vault header is not found (i.e. the file is malformed).

  Returns:
    The SHA256 checksum of the OpenCore binary.
  """

  # Copy the file contents to the temporary file
  file_path = PathResolver(file_path)
  with NamedTemporaryFile(mode="r+b",
                          suffix='-OpenCore.efi',
                          dir=UNPACK_DIR) as f:
    copyfile(file_path.resolve(), f.name)
    file_checksum = file_path.checksum
    f.seek(0)

    # Get the offset of the vault header
    vault_header = b'=BEGIN OC VAULT='
    with mmap(f.fileno(), 0, PROT_READ) as mf:
      offset = mf.find(vault_header)
      if offset != -1:
        f.seek(offset + len(vault_header))
      else:
        raise RuntimeError('No vault header found in the file')

    # Extract and replace the public key
    public_key = f.read(528)
    if has_public_key := any(byte for byte in public_key):
      f.seek(offset + len(vault_header))
      f.write(b'\x00' * 528)

    # Compute the de-vaulted checksum
    checksum = get_stream_digest(stream=f, algorithm=algorithm)

    # Verify that the extraction is reversible
    if has_public_key:
      f.seek(offset + len(vault_header))
      f.write(public_key)
    if not file_checksum == get_stream_digest(stream=f, algorithm=algorithm):
      raise AssertionError('Checksum extraction failed')

  return checksum


__all__ = [
  # Constants (1)
  "OPENCORE_BINARY_DATA_URL",
  # Functions (3)
  "extract_opencore_archive",
  "extract_opencore_directory",
  "get_opencore_checksum"
]
