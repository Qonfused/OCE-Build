## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Methods for retrieving and handling Kext packages and binaries."""

from collections import OrderedDict
from itertools import chain

from typing import List, Literal, Union

from ocebuild.parsers.dict import nested_get
from ocebuild.parsers.plist import parse_plist
from ocebuild.sources.resolver import PathResolver
from ocebuild.versioning.semver import get_version, sort_dependencies


def parse_kext_plist(filepath: Union[str, PathResolver]) -> dict:
  """Parses the Info.plist of a Kext."""
  with open(filepath, 'r', encoding='UTF-8') as file:
    # Build plist dictionary from filestream
    plist = parse_plist(file)

  # Extract Kext bundle properties
  name = nested_get(plist, ['CFBundleName'])
  identifier = nested_get(plist, ['CFBundleIdentifier'])
  version = nested_get(plist, ['CFBundleVersion'])
  executable = nested_get(plist, ['CFBundleExecutable'])
  dependencies = nested_get(plist, ['OSBundleLibraries'], default={})

  return {
    "name": name,
    "identifier": identifier,
    "version": version,
    "executable": executable,
    "dependencies": dependencies
  }

def sort_kext_cfbundle(filepaths: List[Union[str, PathResolver]]) -> OrderedDict:
  """Sorts the injection order of Kexts based on their CFBundleidentifier.

  This implementation uses a topological sort to order Kexts based on their
  CFBundleidentifiers and versions. This handles duplicate versions across
  kexts and their dependencies and ensures that Kexts are injected in the
  correct order with respect to their dependencies and notes their resolved
  minimum required versions.

  Dependent Kexts are always injected before their dependents, and duplicate
  CFBundleIdentifier dependencies are inserted in order of the latest version
  strings. Additionally, any bundled Kexts are grouped with their parent Kexts.

  Args:
    filepaths: A list of filepaths to Kext *.kext files.

  Raises:
    ValueError: If a Kext is missing a CFBundleidentifier key or a dependency.

  Returns:
    An sorted dictionary array of Kexts sorted by their CFBundleIdentifier.
  """
  plist_paths = list(chain(*(PathResolver(f).glob('**/Info.plist')
                             for f in filepaths)))
  kext_names = list(PathResolver(str(f).rsplit('.kext')[-2]).stem
                    for f in plist_paths)

  # Extract flat tree of Kext dependencies
  identifier_map = {}
  dependency_tree = OrderedDict()
  for name, filepath in zip(kext_names, plist_paths):
    plist_props = parse_kext_plist(filepath)
    key = plist_props['identifier']
    if not key:
      raise ValueError(f'Kext missing identifier: {name}')

    # Add Kext to dependency tree
    entries = plist_props['dependencies']
    dependencies = list((k, entries[k]) for k in set(entries.keys()))
    if not key in dependency_tree:
      dependency_tree[key] = dependencies
    # Merge dependencies from duplicate identifiers
    else:
      dependency_tree[key] += dependencies

    # Add Kext to identifier map
    kext_path = filepath.parents[1].as_posix()
    relative_path = ".kext".join(p if i else PathResolver(p).stem for
                                 i,p in enumerate(kext_path.split('.kext')))
    identifier_entry = dict(__path=relative_path, name=name, props=plist_props)
    if not key in identifier_map:
      identifier_map[key] = [identifier_entry]
    else:
      identifier_map[key].append(identifier_entry)

  # Set allow list for unresolved dependencies
  allow_list = { 'com.apple.' }

  # Resolve Kext dependency versions to determine load order
  sorted_dependencies = []
  sorting_scheme = lambda e: get_version(nested_get(e, ['props', 'version'],
                                                    default='latest'))
  for identifier, version in sort_dependencies(dependency_tree):
    # Handle unresolved dependencies
    entries = identifier_map.get(identifier, [])
    if not (entries or any(identifier.startswith(p) for p in allow_list)):
      raise ValueError(f'Unresolved Kext identifier: {identifier}')

    # Handle duplicate identifiers and sort by version
    for entry in sorted(entries, key=sorting_scheme, reverse=True):
      # Flatten plist properties
      plist_props = entry.get('props', {})
      del entry['props']
      entry = { **plist_props, **entry }

      # Set resolved version
      entry['version_required'] = version or None

      # Filter previous entries to determine whether bundled kexts are present
      path = entry['__path']
      parent_kext = path.split('.kext', maxsplit=1)[0] + '.kext'
      bundled_entries = list(e for e in sorted_dependencies
                             if e['__path'].startswith(parent_kext))

      # Group bundled plugins with their parent Kext
      if bundled_entries:
        insertion_index = sorted_dependencies.index(bundled_entries[-1])
        sorted_dependencies.insert(1 + insertion_index, entry)
      # Handle standalone Kexts
      elif not version and (dependencies := entry['dependencies']):
        insertion_index = 0
        for identifier in (dependency_keys := set(dependencies.keys())):
          # Grab the last entry with the same identifier
          matches = list(filter(lambda x: x['identifier'] == identifier,
                                sorted_dependencies))
          if matches:
            dependency_idx = sorted_dependencies.index(matches[-1])
            insertion_index = max(insertion_index, dependency_idx)
          # Grab the last entry with the same mutual dependencies
          try:
            while True:
              next_entry = sorted_dependencies[insertion_index + 1]
              if set(next_entry['dependencies'].keys()) == dependency_keys:
                insertion_index += 1
              else:
                break
          except IndexError:
            pass #de-op
        # Upsert standalone dependents with dependencies/mutual dependents
        if insertion_index:
          sorted_dependencies.insert(1 + insertion_index, entry)
        # Otherwise add entry to sorted dependencies
        else:
          sorted_dependencies.append(entry)
      # Handle dependencies
      else:
        sorted_dependencies.append(entry)

  return sorted_dependencies

def extract_kexts(directory: Union[str, PathResolver],
                  build: Literal['RELEASE', 'DEBUG']='RELEASE',
                  ) -> dict:
  """Extracts the metadata of all Kexts in a directory."""
  kexts = {}
  for plist_path in directory.glob('**/*.kext/**/Info.plist'):
    parent = str(plist_path).rsplit('.kext', maxsplit=1)[0]
    kext_path = PathResolver(f'{parent}.kext')
    extract_path = f'.{kext_path.as_posix().split(directory.as_posix())[1]}'
    # Update kext dictionary
    kexts[kext_path.stem] = {
      "__path": extract_path,
      "__extracted": kext_path,
    }

  # Filter build targets if provided in extract path
  if any(build.lower() in e['__path'].lower() for e in kexts.values()):
    kexts = { k:v for k,v in kexts.items()
              if build.lower() in v['__path'].lower() }

  return kexts


__all__ = [
  # Functions (3)
  "parse_kext_plist",
  "sort_kext_cfbundle",
  "extract_kexts"
]
