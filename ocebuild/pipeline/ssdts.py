## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Methods for retrieving and handling SSDT binaries."""

from collections import OrderedDict
from contextlib import contextmanager
from functools import partial
from graphlib import TopologicalSorter
from os import unlink
from tempfile import NamedTemporaryFile

from typing import Callable, Generator, List, Optional, Union

from ocebuild.parsers.asl import parse_ssdt_namespace
from ocebuild.sources import request
from ocebuild.sources.binary import get_binary_ext, wrap_binary
from ocebuild.sources.github import github_file_url
from ocebuild.sources.resolver import PathResolver


@contextmanager
def extract_iasl_binary(url: Optional[str]=None,
                        persist: bool=False
                        ) -> Generator[Callable[[List[str]], str], any, None]:
  """Extracts an iasl binary and yields a subprocess wrapper."""
  binary = f'iasl{get_binary_ext()}'
  tmp_file = NamedTemporaryFile(suffix=f'-{binary}', delete=False)
  try:
    # Fetch the iasl binary appropriate for the current platform
    if not url:
      url = github_file_url('Qonfused/OCE-Build',
                            path=f'scripts/lib/iasl/{binary}',
                            #TODO: Remove hardcoded commit when PR is merged.
                            commit='448fd871d7de446b894770afb8e0d4b6b5dbbaec', 
                            raw=True)
    # Fetch and extract the iasl binary to a temporary file
    with request(url) as response:
      tmp_file.seek(0)
      tmp_file.write(response.read())
      tmp_file.close()
    # Yield a wrapper over the iasl binary
    yield partial(wrap_binary, binary_path=tmp_file.name)
  finally:
    # Cleanup after context exits
    if not persist: unlink(tmp_file.name)

def sort_ssdt_symbols(filepaths: List[Union[str, PathResolver]]) -> OrderedDict:
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
  # Functions (2)
  "extract_iasl_binary",
  "sort_ssdt_symbols"
]
