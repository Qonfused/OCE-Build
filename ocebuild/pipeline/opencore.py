## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Methods for retrieving and handling OpenCore packages."""

from hashlib import sha256
from shutil import copy, copyfile, copytree
from tempfile import mkdtemp, NamedTemporaryFile

from typing import Generator, Iterator, Literal, Optional, Union

from mmap import mmap, PROT_READ

from .lock import prune_resolver_entry

from ocebuild.filesystem.cache import UNPACK_DIR
from ocebuild.filesystem.posix import glob, move, remove
from ocebuild.sources.binary import get_stream_digest
from ocebuild.sources.resolver import PathResolver


def extract_opencore_archive(pkg: PathResolver,
                             target: Literal['IA32', 'X64']='X64'):
  """Extracts the contents of an OpenCore archive to a temporary directory."""
  tmp_dir = mkdtemp(dir=UNPACK_DIR)

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

  # Overwrite package directory with changes
  remove(pkg)

  return PathResolver(EFI_DIR.parent)

def extract_ocbinary_archive(pkg: PathResolver, oc_pkg: PathResolver) -> None:
  """Extracts OcBinaryData resources to an existing OpenCore archive."""
  for dir_ in oc_pkg.joinpath('EFI', 'OC').iterdir():
    extract = glob(pkg, pattern=f'**/{dir_.name}/', first=True)
    if extract and extract.exists():
      copytree(extract, dir_, dirs_exist_ok=True)
  # Cleanup
  remove(pkg)

def _iterate_entries(opencore_pkg: PathResolver,
                     opencore_dir: PathResolver
                     ) -> Generator[PathResolver, any, None]:
  """Iterate over the entries in the build configuration."""
  for category in map(lambda p: p.name, opencore_dir.iterdir()):
    if category not in ('ACPI', 'Drivers', 'Kexts', 'Tools'): continue
    for path in map(lambda p: p.relative_to(opencore_pkg).as_posix(),
                    opencore_dir.joinpath(category).iterdir()):
      yield path

def prune_opencore_archive(opencore_pkg: PathResolver,
                           resolvers: dict,
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

  oc_dir = opencore_pkg.joinpath('EFI', 'OC')
  # Handle interactive mode for iterator
  iterator = set(_iterate_entries(opencore_pkg, oc_dir))
  num_entries = len(iterator)
  if __wrapper is not None: iterator = __wrapper(iterator, *args, **kwargs)

  # Iterate over the entries in the extracted OpenCore package
  bundled = set(v['__filepath'] for v in resolvers if v['specifier'] == '*')
  for idx, path in enumerate(iterator):
    # Include only binaries that are specified as bundled in the build config
    if path not in bundled:
      remove(opencore_pkg.joinpath(path))
    else:
      #TODO: Add entry under OpenCore's `bundled` property
      bundled.discard(path)
      prune_resolver_entry(resolvers, key='name', value=PathResolver(path).stem)
    # Copy the remaining files to the output directory
    if idx + 1 == num_entries: # This stalls the iterator until completion
      copytree(opencore_pkg, out_dir, dirs_exist_ok=True)
      remove(opencore_pkg)
      return PathResolver(out_dir, oc_dir.relative_to(opencore_pkg))

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
  # Functions (4)
  "extract_opencore_archive",
  "extract_ocbinary_archive",
  "prune_opencore_archive",
  "get_opencore_checksum"
]
