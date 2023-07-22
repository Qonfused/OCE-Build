## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Methods for handling and manipulating the build configuration."""

from itertools import chain
from shutil import unpack_archive
from tempfile import mkdtemp

from typing import Iterator, List, Optional, Tuple

from ocebuild.filesystem import copy, remove
from ocebuild.filesystem.archives import extract_archive
from ocebuild.filesystem.cache import UNPACK_DIR
from ocebuild.parsers.dict import nested_get, nested_set
from ocebuild.parsers.yaml import parse_yaml
from ocebuild.pipeline import kexts
from ocebuild.sources.resolver import PathResolver


def _set_var_default(build_vars: dict, name: str, default: str):
  """Set a variable to a default value if it is not already set."""
  if not (variable := nested_get(build_vars, ['variables', name])):
    variable = default
    nested_set(build_vars, ['variables', name], variable)
  return variable

def read_build_file(filepath: str,
                    normalize_entries: bool=True
                    ) -> Tuple[dict, dict, List[str]]:
  """Read the build configuration from the specified build file.

  Args:
    filepath: The path to the build file.
    normalize_entries: Whether to normalize the entries in the build file.

  Returns:
    A tuple containing:
      - The build configuration.
      - The build variables.
      - The build flags.
  """
  with open(filepath, 'r', encoding='UTF-8') as f:
    build_config, build_vars = parse_yaml(f, frontmatter=True)

  # Extract the OpenCore build configuration
  version = _set_var_default(build_vars, 'version', 'latest')
  build = _set_var_default(build_vars, 'build', 'RELEASE')
  target = _set_var_default(build_vars, 'target', 'X64')

  # Add additional flags from the build configuration
  flags = nested_get(build_vars, ['flags'])
  if build not in flags:  flags += [build]
  if target not in flags: flags += [target]

  # Normalize the entries in the build configuration
  if normalize_entries:
    build_config['OpenCorePkg'] = {
      'OpenCore': {
        '__filepath': 'EFI/OC/OpenCore.efi',
        'specifier': version,
        'repository': 'acidanthera/OpenCorePkg',
        'build': build
      },
      'OcBinaryData': {
        '__filepath': 'EFI/OC/.',
        'specifier': 'latest',
        'repository': 'acidanthera/OcBinaryData',
        'branch': 'master',
        'build': build,
        'tarball': True
      }
    }
    for category, entries in build_config.items():
      # Reconstruct an equivalent dictionary entry
      if isinstance(entries, list):
        build_config[category] = {}
        entries = { k: '*' for k in entries }
      # Normalize the specifier for each entry
      if isinstance(entries, dict):
        for name, entry in entries.items():
          # Handle string specifiers
          if not isinstance(entry, dict):
            build_config[category][name] = {}
            nested_set(build_config, [category, name, 'specifier'], entry)

  return build_config, build_vars, flags

def unpack_build_entries(resolvers: List[dict],
                         project_dir: PathResolver,
                         *args,
                         __wrapper: Optional[Iterator]=None,
                         **kwargs) -> dict:
  """Unpacks the build entries from the build configuration."""

  # Handle interactive mode for iterator
  iterator = resolvers
  if __wrapper is not None: iterator = __wrapper(iterator, *args, **kwargs)

  extracted = {}
  for entry in iterator:
    tmpdir: PathResolver
    # Handle extracting remote entries
    if (url := entry.get('url')):
      with extract_archive(url, persist=True) as tmpdir:
        for archive in tmpdir.glob('**/*.zip'):
          unpack_archive(archive, tmpdir.joinpath(archive.name))
    # Handle extracting local entries
    elif (path := entry.get('path')):
      tmpdir = PathResolver(mkdtemp(dir=UNPACK_DIR))
      src = project_dir.joinpath(path)
      copy(src, tmpdir.joinpath(tmpdir, src.name))
    # Skip wildcard specifiers
    elif entry.get('specifier') == '*': continue
    # Update extracted paths
    entry['__extracted'] = tmpdir
    nested_set(extracted, [entry['__category'], entry['name']], tmpdir)

  return extracted

def _iterate_extract_entries(unpacked_entries: dict):
  """Iterate over the entries in the build configuration."""
  def group_entries(category: str, entries: dict):
    return [(category, name, tmpdir) for name, tmpdir in entries.items()]
  return list(chain(*[group_entries(c,e) for c,e in unpacked_entries.items()]))

def extract_build_entries(build_vars: dict,
                          lockfile: dict,
                          unpacked_entries: dict,
                          build_dir: PathResolver,
                          *args,
                          __wrapper: Optional[Iterator]=None,
                          **kwargs
                          ) -> dict:
  """Extracts packages from unpacked package entries."""

  # Handle interactive mode for iterator
  iterator = _iterate_extract_entries(unpacked_entries)
  if __wrapper is not None: iterator = __wrapper(iterator, *args, **kwargs)

  extracted = {}
  for (category, name, tmpdir) in iterator:
    # Extract SSDTs from the archive
    if   category == 'ACPI':
      pass
    # Extract kexts from the archive
    elif category == 'Kexts':
      build = nested_get(lockfile, ['dependencies', name, 'build'],
                          default=build_vars['variables']['build'])
      extract = kexts.extract_kexts(tmpdir, build=build)
      # Filter out plugins that are not bundled
      extracted_kexts = []
      for k_name, kext in extract.items():
        is_plugin = '.kext/' in kext['__extract']
        # Add kexts to the extracted entries
        if not is_plugin:
          kext['__dest'] = build_dir.joinpath(f'{k_name}.kext')
          extracted_kexts.append((k_name, kext))
        # Prune implicitly excluded plugins
        elif (bundled := kext.get('bundled')):
          if k_name not in bundled: remove(kext['__path'])
      # Add the extracted kexts to the build
      for k,e in extracted_kexts:
        k_name = name if len(extracted_kexts) == 1 else k
        nested_set(extracted, [category, k_name], e)
    # Extract drivers or tools from the archive
    elif category in ('Drivers', 'Tools'):
      pass
    # Extract resources from the archive
    elif category == 'Resources':
      pass

  return extracted

__all__ = [
  # Functions (3)
  "read_build_file",
  "unpack_build_entries",
  "extract_build_entries"
]
