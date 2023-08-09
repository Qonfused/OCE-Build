## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Methods for sorting and handling versioning."""

from collections import OrderedDict
from graphlib import TopologicalSorter
from itertools import chain

from typing import Dict, Generator, List, Set, Tuple, Union

from packaging import version as vpkg

from ocebuild.parsers.regex import re_search


SEMVER_SYMBOLS      = ('~', '^')
"""Semantic versioning range symbols."""

COMPARISON_SYMBOLS  = ('>', '<', '>=', '<=', '==', '!=')
"""Version comparison symbols."""

def get_version_str(string: str) -> Union[str, None]:
  """Gets the version string from a version specifier.

  Args:
    string: The version specifier.

  Returns:
    The version string.

  Example:
    >>> get_version_string('^1.0.0')
    # -> '1.0.0'
    >>> get_version_string('1.0.0')
    # ->'1.0.0'
    >>> get_version_string('latest')
    # -> None
  """
  # Remove non-standard release tags
  string = string\
    .replace('-prerelease', '') \
    .replace('-release', '') \
    .replace('-debug', '') \
    .replace('-stable', '')
  # Remove semver versioning symbols
  for symbol in reversed([*SEMVER_SYMBOLS, *COMPARISON_SYMBOLS]):
    if symbol in string[:len(symbol)]:
      return string[len(symbol):]
  return string

def get_version(string: str) -> Union[vpkg.Version, None]:
  """Gets the version class from a version specifier.

  Args:
    string: The version class.

  Returns:
    The version string.

  Example:
    >>> get_version('^1.0.0')
    # -> <Version('1.0.0')>
    >>> get_version('1.0.0')
    # -> <Version('1.0.0')>
    >>> get_version('latest')
    # -> None
  """

  # Try using the packaging parse method
  version_str = get_version_str(string)
  try:
    return vpkg.parse(version_str)
  except vpkg.InvalidVersion: pass
  # Fallback to regex parsing
  if version_str := re_search(r'[0-9][0-9.]*', version_str):
    try:
      return vpkg.parse(version_str)
    except Exception: pass

def compare_version(v1: Union[str, vpkg.Version],
                    v2: Union[str, vpkg.Version],
                    operator: str
                    ) -> bool:
  """Compares a version to the version specifier.

  Args:
    v1: The version.
    v2: The version specifier.
    operator: The operator.

  Returns:
    True if the version satisfies the specifier.
  """
  v1_arr = get_version(v1) if isinstance(v1, str) else v1
  v2_arr = get_version(v2) if isinstance(v2, str) else v2
  if operator == '>':   return v1_arr >  v2_arr
  if operator == '<':   return v1_arr <  v2_arr
  if operator == '>=':  return v1_arr >= v2_arr
  if operator == '<=':  return v1_arr <= v2_arr
  if operator == '==':  return v1_arr == v2_arr
  if operator == '!=':  return v1_arr != v2_arr
  return False

def resolve_version_specifier(versions: List[str],
                              specifier: str
                              ) -> Union[str, None]:
  """Resolves a version specifier.

  Args:
    versions: The versions.
    specifier: The version specifier.

  Returns:
    The resolved version (if available).

  Examples:
    >>> resolve_version_specifier(['1.2.3', '1.2.4', '1.3.0'], '~1.2.3')
    # -> '1.2.4'
    >>> resolve_version_specifier(['1.2.3', '1.3.0', '2.0.0'], '^1.2.3')
    # -> '1.3.0'
    >>> resolve_version_specifier(['1.2.3', '1.2.4', '1.3.0'], '1.2.3')
    # -> '1.2.3'
    >>> resolve_version_specifier(['1.2.3', '1.2.4', '1.3.0'], '>1.2.3')
    # -> '1.3.0'
    >>> resolve_version_specifier(['1.2.2', '1.2.3', '1.3.0'], '<1.2.3')
    # -> '1.2.2'
    >>> resolve_version_specifier(['1.2.3', '1.2.4', '1.3.0'], '>=1.2.3')
    # -> '1.3.0'
    >>> resolve_version_specifier(['1.2.3', '1.2.4', '1.3.0'], '<=1.2.3')
    # -> '1.2.3'
    >>> resolve_version_specifier(['1.2.3', '1.2.4', '1.3.0'], '!=1.2.3')
    # -> '1.3.0'
    >>> resolve_version_specifier(['1.2.3', '1.2.4', '1.3.0'], '==1.2.3')
    # -> '1.2.3'
    >>> resolve_version_specifier(['1.2.3', '1.2.4', '1.3.0'], 'latest')
    # -> '1.3.0'
    >>> resolve_version_specifier(['1.2.3', '1.2.4', '1.3.0'], 'oldest')
    # -> '1.2.3'
    >>> resolve_version_specifier(['1.2.3', '1.2.4', '1.3.0'], '1.2.2')
    # -> None
  """
  # Sort available versions
  sorted_versions = sorted(set(get_version(v) for v in versions if v))
  # Handle named specifiers
  if specifier == 'latest': return str(sorted_versions[-1])
  if specifier == 'oldest': return str(sorted_versions[0])

  # Find the version in the sorted list
  version_str = get_version_str(specifier)
  version = get_version(version_str)
  if not version: return None
  # Parse semver symbols
  symbol = specifier[:specifier.index(version_str if version_str else '')]
  # Up to next minor
  # e.g. '~1.2.3' -> '>=1.2.3,<1.3.0'
  if symbol == '~':
    filtered = [v for v in sorted_versions
                if compare_version(v, version, operator='>=')
                  and v.major == version.major
                  and v.minor < version.minor+1]
    if len(filtered): return str(filtered[-1])
  # Up to next major
  # e.g. '^1.2.3' -> '>=1.2.3,<2.0.0'
  elif symbol == '^':
    filtered = [v for v in sorted_versions
                if compare_version(v, version, operator='>=')
                  and v.major < version.major+1]
    if len(filtered): return str(filtered[-1])
  # Direct comparisons
  elif symbol in COMPARISON_SYMBOLS:
    filtered = [v for v in sorted_versions
                if compare_version(v, version, operator=symbol)]
    if len(filtered): return str(filtered[-1])
  # Fallthrough
  else:
    # Exact match
    # e.g. '1.2.3' -> '==1.2.3'
    filtered = [v for v in sorted_versions
                if compare_version(v, version, operator='==')]
    if len(filtered): return str(filtered[-1])
  # No match
  return None

def get_minimum_version(dependencies: Dict[str, Tuple[str, str]],
                        library: str
                        ) -> Tuple[str, Union[str, None]]:
  """Gets the minimum required version of a library.

  Args:
    dependencies: The dependency tree.
    library: The library to get the minimum version of.

  Returns:
    A tuple of the library name and the minimum version.

  Example:
    >>> dependencies = {
    ...   'lib1': [('lib2', '2.0.0')],
    ...   'lib2': [('lib3', '3.0.0')],
    ...   'lib3': [],
    ... }
    >>> get_minimum_version(dependencies, 'lib1')
    # -> ('lib1', None)
    >>> get_minimum_version(dependencies, 'lib2')
    # -> ('lib2', '^2.0.0')
    >>> get_minimum_version(dependencies, 'lib3')
    # -> ('lib3', '^3.0.0')
  """
  versions = set(k[1] for k in list(chain(*dependencies.values()))
                 if k[0] == library)
  (versions := list(versions)).sort(key=get_version)
  return (library, f'^{str(versions[-1])}' if versions else None)

def _sort_static_tree(dependencies: Dict[str, Tuple[str, str]]
                      ) -> Dict[str, Set[str]]:
  """Sorts the insertion order for dependencies before topological sorting."""

  dependency_tree = { k: set(v[0] for v in t) for k,t in dependencies.items() }

  # Determines the weight of a dependency tree node for insertion.
  num_dependencies = {}
  num_dependents = {}
  for key, links in dependency_tree.items():
    num_dependencies[key] = sum(1 if l in dependencies else 0 for l in links)
    for l in links:
      if l in num_dependents:
        num_dependents[l] += 1
      else:
        num_dependents[l] = 1

  # Sorts the dependency tree by the updated weights.
  dependency_tree = OrderedDict(sorted(dependency_tree.items(),
                                       key=lambda t: (
                                         -num_dependents.get(t[0], 0),
                                         -num_dependencies.get(t[0], 0),
                                         t[0],
                                         t[1]
                                       )))
  return dependency_tree

def sort_dependencies(dependencies: Dict[str, Tuple[str, str]],
                     ) -> Generator[Tuple[str, str], any, None]:
  """Sorts a dependency tree by topology and version.

  Args:
    dependencies: The dependency tree.

  Yields:
    A tuple of the library name and the minimum version.

  Raises:
    ValueError: If a cycle is detected in the dependency tree.

  Example:
    >>> dependencies = {
    ...   'lib1': [('lib2', '2.0.0')],
    ...   'lib2': [('lib3', '3.0.0')],
    ...   'lib3': [],
    ... }
    >>> list(sort_dependencies(dependencies))
    # -> [('lib3', '^3.0.0'), ('lib2', '^2.0.0'), ('lib1', None)]
  """

  # Sort dependency tree by dependency weights
  dependency_tree = _sort_static_tree(dependencies)

  # for library in TopologicalSorter(dependency_tree).static_order():
  #   yield get_minimum_version(dependencies, library)

  static_dependency_tree = []
  self = TopologicalSorter(dependency_tree)
  self.prepare()
  invalid_nodes = set()
  while self.is_active():
    node_group = self.get_ready()
    # Handle invalid hoists of zero-dependency nodes
    if not (static_dependency_tree or invalid_nodes):
      invalid_nodes |= set(n for n in node_group
                           if dependency_tree.get(n, None) == set())
    # Add nodes to static dependency tree
    for node in node_group:
      if node not in invalid_nodes:
        static_dependency_tree.append(node)
    # Mark nodes as processed
    self.done(*node_group)

  # Append invalid-hoisted nodes to static dependency tree
  for node in invalid_nodes:
    static_dependency_tree.append(node)

  for library in static_dependency_tree:
    yield get_minimum_version(dependencies, library)


__all__ = [
  # Constants (2)
  "SEMVER_SYMBOLS",
  "COMPARISON_SYMBOLS",
  # Functions (6)
  "get_version_str",
  "get_version",
  "compare_version",
  "resolve_version_specifier",
  "get_minimum_version",
  "sort_dependencies"
]
