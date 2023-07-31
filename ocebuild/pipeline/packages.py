#!/usr/bin/env python3

## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Methods for retrieving and handling packages."""

from functools import reduce
from itertools import chain

from typing import Iterator, List, Optional, Union

from ocebuild.filesystem import glob, remove
from ocebuild.parsers.dict import merge_dict, nested_del, nested_get, nested_set
from ocebuild.pipeline import config, kexts, opencore, ssdts
from ocebuild.pipeline.lock import _category_extension, prune_resolver_entry

from third_party.cpython.pathlib import Path


def extract_opencore_packages(opencore_pkg: Union[str, Path],
                              target: str,
                              resolvers: List[dict],
                              packages: dict,
                              ) -> dict:
  """Extracts build entries as vendored packages from an OpenCore package.

  Args:
    opencore_pkg: Path to an existing OpenCore package.
    target: The desired target architecture of the OpenCore EFI.
    resolvers: The list of resolver entries to update.
    packages: The list of packages to update.

  Returns:
    A dictionary of extracted build entries.
  """

  # Replace archive temporary directory with extracted contents
  opencore.extract_opencore_archive(opencore_pkg, target)
  # Extract additional OpenCore binaries not shipped in the main package
  if binary_pkg := nested_get(packages, ['OpenCorePkg', 'OcBinaryData']):
    opencore.extract_ocbinary_archive(pkg=binary_pkg, oc_pkg=opencore_pkg)
    nested_del(packages, ['OpenCorePkg', 'OcBinaryData'])

  # Cleanup resolver entries
  prune_resolver_entry(resolvers, key='__category', value='OpenCorePkg')

  # Extract build entries from the OpenCore package as (vendored) packages
  extracted = opencore.extract_build_entries(opencore_pkg, resolvers)

  return extracted

def _iterate_extract_packages(unpacked_entries: dict):
  """Iterate over the entries in the build configuration."""
  def group_entries(category: str, entries: dict):
    return [(category, name, tmpdir) for name, tmpdir in entries.items()]
  return list(chain(*[group_entries(c,e) for c,e in unpacked_entries.items()]))

def extract_build_packages(build_vars: dict,
                           resolvers: List[dict],
                           packages: dict,
                           build_dir: Path,
                           *args,
                           __wrapper: Optional[Iterator]=None,
                           **kwargs
                           ) -> dict:
  """Extracts build entries from unpacked packages.

  Args:
    build_vars: The configured build variables.
    resolvers: The list of resolver entries to update.
    packages: The list of packages to extract.
    build_dir: The path to the build directory.
    *args: Additional arguments to pass to the iterator.
    __wrapper: A wrapper function to apply to the iterator. (Optional)
    **kwargs: Additional keyword arguments to pass to the iterator.

  Returns:
    A dictionary of extracted build entries.
  """

  def _get_resolver_entry(category: str, name: str) -> Union[dict, None]:
    return next(filter(lambda e: e['__category'] == category and
                                 e['name'] == name,
                       resolvers), None)

  # Extract build variables
  default_build = build_vars['variables']['build']

  # Handle interactive mode for iterator
  iterator = _iterate_extract_packages(packages)
  if __wrapper is not None: iterator = __wrapper(iterator, *args, **kwargs)

  # Extract build entries from the remaining packages
  extracted_entries = {}
  for (category, name, tmpdir) in iterator:
    ext, _ = _category_extension(category)
    resolver_entry = _get_resolver_entry(category, name)
    # Extract SSDTs from the archive
    if   category == 'ACPI':
      extract = ssdts.extract_ssdts(tmpdir)
    # Extract kexts from the archive
    elif category == 'Kexts':
      entry_build = resolver_entry.get('build') or default_build
      extract = kexts.extract_kexts(tmpdir, build=entry_build)
      # Filter out plugins that are not bundled
      for k_name, kext in extract.copy().items():
        # Exclude plugins that are already bundled
        is_plugin = '.kext/' in kext['__path']
        if is_plugin:
          nested_del(extract, [k_name])
        else: continue
        # Prune implicitly excluded plugins
        if (bundled := kext.get('bundled')):
          if k_name not in bundled:
            remove(kext['__extracted'])
    # Extract drivers or tools from the archive
    elif category in ('Drivers', 'Tools'):
      extract = {}
      for binary_path in glob(tmpdir, f'**/*{ext}'):
        path = f'.{binary_path.as_posix().split(tmpdir.as_posix())[1]}'
        extract[binary_path.name] = {
          '__extracted': binary_path,
          '__path': path
        }
    # Extract resources from the archive
    elif category == 'Resources':
      pass

    # Update extracted paths
    for k,e in extract.items():
      e_name = name if len(extract) == 1 else k
      # Ensure only valid build entries are extracted
      if _get_resolver_entry(category, e_name):
        e['__dest'] = build_dir.joinpath('EFI', 'OC', category, f'{e_name}{ext}')
        nested_set(extracted_entries, [category, e_name], e)

  return extracted_entries

def _iterate_prune_packages(extracted_entries: dict):
  """Iterate over the entries in the build configuration."""
  def group_entries(category: str, entries: dict):
    return [(category, name, entry) for name, entry in entries.items()]
  return list(chain(*[group_entries(c,e) for c,e in extracted_entries.items()]))

def prune_build_packages(build_config: dict,
                         extracted_entries: dict,
                         *args,
                         __wrapper: Optional[Iterator]=None,
                         **kwargs
                         ) -> dict:
  """Prunes the build configuration of entries that were not extracted.

  Args:
    build_config: The build configuration.
    extracted_entries: The extracted build entries.
    *args: Additional arguments to pass to the iterator.
    __wrapper: A wrapper function to apply to the iterator. (Optional)
    **kwargs: Additional keyword arguments to pass to the iterator.

  Returns:
    A dictionary of pruned build entries.
  """

  # Create list of entry names and their bundled package names
  entries = reduce(merge_dict, [
    { c: (k, *nested_get(e, ['bundled'], default=[])) }
      for c,d in build_config.items()
        for k,e in d.items()
  ], {})

  # Handle interactive mode for iterator
  iterator = _iterate_prune_packages(extracted_entries)
  if __wrapper is not None: iterator = __wrapper(iterator, *args, **kwargs)

  for category, name, entry in iterator:
    # Prune extracted entries that are not in the build configuration
    if not name in nested_get(entries, [category], default=()):
      nested_del(extracted_entries, [category, name])
      remove(entry['__extracted'])


__all__ = [
  # Functions (3)
  "extract_opencore_packages",
  "extract_build_packages",
  "prune_build_packages"
]
