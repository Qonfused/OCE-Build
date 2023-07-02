## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Methods for retrieving and handling SSDT binaries."""

from collections import OrderedDict
from graphlib import TopologicalSorter

from typing import List, Union

from ocebuild.parsers.asl import parse_ssdt_namespace
from ocebuild.sources.resolver import PathResolver


def sort_ssdt_symbols(filepaths: List[Union[str, PathResolver]]):
  """Sorts the injection order of SSDT tables by resolving symbolic references.
  
  Args:
    filepaths: A list of filepaths to SSDT files.
  
  Returns:
    An ordered dictionary of SSDT table names with their exported symbols.
  """
  ssdt_names = list(PathResolver(f).stem for f in filepaths)

  # Extract flat tree of SSDT symbols and tables
  dependency_tree = OrderedDict()
  for ssdt, filepath in sorted(zip(ssdt_names, filepaths)):
    with open(filepath, 'r', encoding='UTF-8') as file:
      namespace = parse_ssdt_namespace(file)
    dependency_tree[ssdt] = [k for k in namespace['imports'].keys()]
    for symbol in namespace['statements']:
      if not symbol in dependency_tree:
        dependency_tree[symbol] = [ssdt]
      else:
        dependency_tree[symbol].append(ssdt)
  
  # Sort table load order
  sorted_dependencies = OrderedDict()
  table = 'DSDT'
  for symbol in TopologicalSorter(dependency_tree).static_order():
    # Handle SSDT dependencies
    if symbol in ssdt_names:
      table = symbol
      sorted_dependencies[table] = [s for s,d in dependency_tree.items()
                                    if table in d]
    # Handle DSDT dependencies
    elif not table in sorted_dependencies:
      sorted_dependencies[table] = list()
    elif not table in ssdt_names:
      sorted_dependencies[table].append(symbol)
  
  # Sort table dependencies by root -> alphabetically
  for k, arr in sorted_dependencies.items():
    sorted_dependencies[k] = sorted(arr, key=lambda s: (s.count('.'), s))

  return sorted_dependencies


__all__ = [
  "sort_ssdt_symbols"
]
