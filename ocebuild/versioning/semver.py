## @file
# Methods for sorting and handling versioning.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

from graphlib import TopologicalSorter
from itertools import chain
from re import search as re_search

from typing import Dict, Generator, List, Tuple, Union


def get_version_string(string: str) -> Union[str, None]:
  """Gets the version string from a version specifier.

  Args:
    string: The version specifier.

  Returns:
    The version string.
  
  Example:
    >>> get_version_string('^1.0.0')
    # -> '1.0.0'
    >>> get_version_string('1.0.0')
    # -> '1.0.0'
    >>> get_version_string('latest')
    # -> None
  """
  matches = re_search(r'([\d.]+)', string)
  return matches.group(1) if matches else None

def get_version_parts(version: str) -> List[int]:
  """Gets the version parts from a version string.

  Args:
    version: The version string.

  Returns:
    The version parts.
  
  Example:
    >>> get_version_parts('1.0.0')
    # -> [1, 0, 0]
    >>> get_version_parts('latest')
    # -> None
  """
  parts = get_version_string(version)
  return list(map(int, parts.split('.'))) if parts else list()

def compare_version(v1: str, v2: str, operator: str) -> bool:
  """Compares a version to the version specifier.
  
  Args:
    v1: The version.
    v2: The version specifier.
    operator: The operator.

  Returns:
    True if the version satisfies the specifier.
  """
  v1_arr = get_version_parts(v1)
  v2_arr = get_version_parts(v2)
  if operator == '>':   return v1_arr >  v2_arr
  if operator == '<':   return v1_arr <  v2_arr
  if operator == '>=':  return v1_arr >= v2_arr
  if operator == '<=':  return v1_arr <= v2_arr
  if operator == '==':  return v1_arr == v2_arr
  if operator == '!=':  return v1_arr != v2_arr
  return False

def resolve_version_specifier(versions: List[str],
                              specifier: str) -> Union[str, None]:
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
  sorted_versions = list(set(get_version_string(v) for v in versions))
  sorted_versions.sort(key=lambda s: list(map(int, s.split('.'))))
  # Handle named specifiers
  if specifier == 'latest': return sorted_versions[-1]
  if specifier == 'oldest': return sorted_versions[0]
  
  # Find the version in the sorted list
  version_str = get_version_string(specifier)
  symbol = specifier[:specifier.index(version_str if version_str else '')]
  # Up to next minor
  # e.g. '~1.2.3' -> '>=1.2.3,<1.3.0'
  if symbol == '~':
    filtered = [v for v in sorted_versions
                if compare_version(v, version_str, operator='>=')
                and get_version_parts(v)[0] == get_version_parts(version_str)[0]
                and get_version_parts(v)[1] < get_version_parts(version_str)[1]+1]
    if len(filtered): return filtered[-1]
  # Up to next major
  # e.g. '^1.2.3' -> '>=1.2.3,<2.0.0'
  elif symbol == '^':
    filtered = [v for v in sorted_versions
                if compare_version(v, version_str, operator='>=')
                and get_version_parts(v)[0] < get_version_parts(version_str)[0]+1]
    if len(filtered): return filtered[-1]
  # Direct comparisons
  elif symbol in ('>', '<', '>=', '<=', '==', '!='):
    filtered = [v for v in sorted_versions
                if compare_version(v, version_str, operator=symbol)]
    if len(filtered): return filtered[-1]
  # Fallthrough
  else:
    # Exact match
    # e.g. '1.2.3' -> '==1.2.3'
    if specifier == version_str:
      filtered = [v for v in sorted_versions
                  if compare_version(v, version_str, operator='==')]
      if len(filtered): return filtered[-1]
    # No match
    return None

def get_minimum_version(dependencies: Dict[str, Tuple[str, str]],
                        library: str) -> Tuple[str, Union[str, None]]:
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
  (versions := list(versions)).sort(key=lambda s: list(map(int, s.split('.'))))
  return (library, f'^{versions[-1]}' if len(versions) else None)

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
  dependency_tree = { k: set(v[0] for v in t) for k,t in dependencies.items() }
  for library in TopologicalSorter(dependency_tree).static_order():
    yield get_minimum_version(dependencies, library)
