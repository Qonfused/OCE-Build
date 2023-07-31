## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Methods for retrieving and handling OpenCore packages."""

from hashlib import sha256
from shutil import copyfile, copytree
from tempfile import mkdtemp, NamedTemporaryFile

from typing import Generator, Iterator, List, Literal, Optional, Tuple, Union

from mmap import mmap, PROT_READ

from .lock import prune_resolver_entry

from ocebuild.filesystem.cache import UNPACK_DIR
from ocebuild.filesystem.posix import glob, move, remove
from ocebuild.parsers.dict import nested_get, nested_set
from ocebuild.sources.binary import get_stream_digest

from third_party.cpython.pathlib import Path


def extract_opencore_archive(pkg: Path,
                             target: Literal['IA32', 'X64']='X64') -> None:
  """Extracts the contents of an OpenCore archive to a temporary directory.

  Args:
    pkg: Path to an existing OpenCore package.
    target: The desired target architecture of the OpenCore EFI.
  """
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
  move(sample_plist, DOCS_DIR)

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
  for dir_ in Path(tmp_dir).iterdir():
    move(dir_, pkg)

def extract_ocbinary_archive(pkg: Path, oc_pkg: Path) -> None:
  """Extracts OcBinaryData resources to an existing OpenCore archive.

  Args:
    pkg: Path to an existing OcBinarData archive.
    oc_pkg: Path to an existing OpenCore package.
  """
  for dir_ in oc_pkg.joinpath('EFI', 'OC').iterdir():
    extract = glob(pkg, pattern=f'**/{dir_.name}/', first=True)
    if extract and extract.exists():
      copytree(extract, dir_, dirs_exist_ok=True)
  # Cleanup
  remove(pkg)

def _iterate_entries(opencore_pkg: Path,
                     opencore_dir: Path
                     ) -> Generator[Tuple[str, str], any, None]:
  """Iterate over the entries in the build configuration."""
  for category in map(lambda p: p.name, opencore_dir.iterdir()):
    if category not in ('ACPI', 'Drivers', 'Kexts', 'Tools'): continue
    for path in map(lambda p: p.relative_to(opencore_pkg).as_posix(),
                    opencore_dir.joinpath(category).iterdir()):
      yield category, path

def extract_build_entries(opencore_pkg: Path,
                          resolvers: List[dict],
                          *args,
                          __wrapper: Optional[Iterator]=None,
                          **kwargs
                          ) -> None:
  """Prunes and extracts build entries from an OpenCore package.

  Args:
    opencore_pkg: The path to the OpenCore package.
    resolvers: The build configuration resolvers.
    *args: Additional arguments to pass to the optional iterator wrapper.
    __wrapper: A wrapper function to apply to the iterator. (Optional)
    **kwargs: Additional keyword arguments to pass to the optional iterator wrapper.

  Returns:
    A Path to the extracted OpenCore directory.
  """

  oc_dir = opencore_pkg.joinpath('EFI', 'OC')
  # Handle interactive mode for iterator
  iterator = set(_iterate_entries(opencore_pkg, oc_dir))
  if __wrapper is not None: iterator = __wrapper(iterator, *args, **kwargs)

  # Iterate over the entries in the extracted OpenCore package
  extract_entries = {}
  bundled = list(filter(lambda e: e['specifier'] == '*', resolvers))
  for category, path in iterator:
    # Include only binaries that are specified as bundled in the build config
    matches = filter(lambda e: str(e['__filepath']).find(path) > 0, bundled)
    if entry := next(matches, None):
      filepath = Path(entry['__filepath']).as_posix()
      prune_resolver_entry(resolvers, key='__filepath', value=filepath)
      # Add the entry to the extracted entries
      relative = f'.{path.rsplit(category, maxsplit=1)[1]}'
      name = nested_get(entry, ['name'], default=Path(path).stem)
      nested_set(extract_entries, [entry['__category'], name], {
        '__dest': Path(filepath),
        '__extracted': Path(opencore_pkg.joinpath(path)),
        '__path': relative
      })
    else:
      remove(opencore_pkg.joinpath(path))

  return extract_entries

def get_opencore_checksum(file_path: Union[str, Path],
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
  file_path = Path(file_path)
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
  "extract_build_entries",
  "get_opencore_checksum"
]
