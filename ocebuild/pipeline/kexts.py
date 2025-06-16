## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Methods for retrieving and handling Kext packages and binaries."""

from collections import OrderedDict
from itertools import chain

from typing import List, Literal, Union

from ocebuild.parsers.dict import nested_get
from ocebuild.parsers.plist import parse_plist
from ocebuild.versioning.semver import get_version, sort_dependencies

from third_party.cpython.pathlib import Path


def parse_kext_plist(filepath: Union[str, Path]) -> dict:
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

def sort_kext_cfbundle(filepaths: List[Union[str, Path]]) -> OrderedDict:
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
  plist_paths = list(chain(*(Path(f).glob('**/Info.plist')
                             for f in filepaths)))
  kext_names = list(Path(str(f).rsplit('.kext')[-2]).name
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
    relative_path = ".kext".join(p if i else Path(p).name for
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
  handled_paths = set()
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

      # Avoid duplicating entries on filepath
      path = entry['__path']
      if not path in handled_paths:
        handled_paths.add(path)
      else: continue

      # Filter previous entries to determine whether bundled kexts are present
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
        for dependency in (dependency_keys := set(dependencies.keys())):
          # Grab the last entry with the same identifier
          matches = list(filter(lambda x: x['identifier'] == dependency,
                                sorted_dependencies))
          if matches:
            dependency_idx = sorted_dependencies.index(matches[-1])
            insertion_index = max(insertion_index, dependency_idx)
          # Grab the last entry with the same mutual dependencies
          try:
            while True:
              next_entry = sorted_dependencies[insertion_index + 1]
              # Next entry has the same dependencies
              has_mutual_keys = dependency_keys == \
                set(next_entry['dependencies'].keys())
              # Next entry shares the current matched dependency
              has_mutual_dependency = dependency in next_entry['dependencies']
              if matches and (has_mutual_keys or has_mutual_dependency):
                insertion_index += 1
              else: break
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

  def num_dependents(kext: dict) -> int:
    return sum(1 if kext['identifier'] in k['dependencies'] else 0
               for k in sorted_dependencies)

  # Group each node alphabetically by dependency name
  offset = 0
  nodes = []
  included = set()
  for idx, kext in enumerate(sorted_dependencies):
    has_resolved_dependencies = any(k in identifier_map
                                    for k in kext.get('dependencies', {}))
    is_bundled_kext = kext['__path'].count('.kext') > 1
    is_standalone_kext = not num_dependents(kext) and not is_bundled_kext

    node_added = False
    # Has no dependencies on any nodes' dependents
    if is_standalone_kext and not has_resolved_dependencies:
      nodes.append([kext])
      included.add(id(kext))
      offset = idx + 1
      node_added = True
    # Has dependents in the current node
    elif num_dependents(kext) and not (is_bundled_kext or offset == idx):
      # Append previous node group if it exists
      prev_node = [k for k in sorted_dependencies[offset:idx] if id(k) not in included]
      if prev_node:
        nodes.append(prev_node)
        for k in prev_node:
          included.add(id(k))
        node_added = True
      # Start new offset for the current kext (which might start a new node later)
      offset = idx
    # Is bundled or has dependencies in the current node (group with previous)
    elif not (has_resolved_dependencies or is_bundled_kext):
      # Append node including current kext, update offset for next group
      node = [k for k in sorted_dependencies[offset : idx + 1] if id(k) not in included]
      if node:
        nodes.append(node)
        for k in node:
          included.add(id(k))
        node_added = True
      offset = idx + 1
    # Ensures the last node is added (includes all remaining kexts)
    elif idx == len(sorted_dependencies) - 1:
      # Append the final node including the last kext
      final_node = [k for k in sorted_dependencies[offset : idx + 1] if id(k) not in included]
      if final_node:
        nodes.append(final_node)
        for k in final_node:
          included.add(id(k))
        node_added = True
    else:
      # Otherwise, continue processing without creating a new node yet
      continue

    # Sort the inserted node's standalone dependents alphabetically, only if a node was added
    if node_added and nodes and nodes[-1]: # Check if nodes is not empty and last node is not empty
      last_node = nodes[-1]
      ordered, unordered = [], []
      for k in last_node:
        (ordered if num_dependents(k) else unordered).append(k)
      # Only replace if the sorting actually changes something or if it's necessary
      nodes[-1] = ordered + sorted(unordered, key=lambda k: k['name'])

  # Ensure all kexts are included in nodes (no dropped/overwritten kexts)
  missing = [k for k in sorted_dependencies if id(k) not in included]
  if missing:
    # Only append if at least one kext in missing is not already included
    if any(id(k) not in included for k in missing):
      nodes.append([k for k in missing if id(k) not in included])
      for k in missing:
        included.add(id(k))

  # Handle colliding cfbundleidentifiers (or unmapped kexts)
  for kext in sorted_dependencies:
    if not any(kext in node for node in nodes):
      for node in nodes:
        for i,k in enumerate(node):
          # If the kext has a duplicate cfbundleidentifier, upsert it before the
          # colliding kext in the node list. Here, we assume that the kexts are
          # never loaded at the same time (i.e. they have exclusive MinKernel
          # and MaxKernel versions).
          if kext['identifier'] == k['identifier']:
            node.insert(i if kext['__path'] < k['__path'] else i + 1, kext)
            break

  # Apply new node sorting scheme to sorted kexts list
  sorted_dependencies = []
  sorting_scheme = lambda n: (n[0]['name'][:3], -len(n))
  for node in sorted(filter(None, nodes), key=sorting_scheme):
    sorted_dependencies += node

  return sorted_dependencies

def extract_kexts(directory: Union[str, Path],
                  build: Literal['RELEASE', 'DEBUG']='RELEASE',
                  ) -> dict:
  """Extracts the metadata of all Kexts in a directory."""
  kexts = {}
  for plist_path in directory.glob('**/*.kext/**/Info.plist'):
    parent = str(plist_path).rsplit('.kext', maxsplit=1)[0]
    kext_path = Path(f'{parent}.kext')
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
