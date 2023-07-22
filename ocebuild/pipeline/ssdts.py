## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Methods for retrieving and handling SSDT binaries and source code."""

from collections import OrderedDict
from contextlib import contextmanager
from functools import partial
from graphlib import TopologicalSorter
from os import unlink
from shutil import copyfile, rmtree, which
from tempfile import mkdtemp, NamedTemporaryFile

from typing import Callable, Generator, List, Optional, Union

from ocebuild.filesystem import glob
from ocebuild.filesystem.cache import UNPACK_DIR
from ocebuild.parsers.asl import parse_ssdt_namespace
from ocebuild.sources import request
from ocebuild.sources.binary import get_binary_ext, wrap_binary
from ocebuild.sources.github import github_file_url
from ocebuild.sources.resolver import PathResolver


@contextmanager
def extract_iasl_binary(url: Optional[str]=None,
                        cache: bool=True,
                        persist: bool=False
                        ) -> Generator[Callable[[List[str]], str], any, None]:
  """Extracts an iasl binary and yields a subprocess wrapper.

  Args:
    url: The URL to the iasl binary.
    cache: Whether to cache the extracted iasl binary.
    persist: Whether to persist the extracted binary.

  Yields:
    A subprocess wrapper for the extracted iasl binary.
  """
  binary = f'iasl{get_binary_ext()}'
  tmp_file = NamedTemporaryFile(suffix=f'-{binary}',
                                delete=not cache,
                                dir=UNPACK_DIR)
  try:
    # Fetch the iasl binary appropriate for the current platform
    if not url:
      url = github_file_url('Qonfused/iASL', path=binary, raw=True)
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

@contextmanager
def iasl_wrapper(cache: bool=True
                 ) -> Generator[Callable[[List[str]], str], any, None]:
  """Returns a subprocess wrapper for an existing or extracted iasl binary.

  By default, this method will attempt to locate an existing iasl binary on the
  system. If one is not found, it will extract a temporary iasl binary from the
  Qonfused/iASL repository.

  Args:
    cache: Whether to cache the extracted iasl binary.

  Yields:
    A subprocess wrapper for the iasl binary.
  """
  tmp_wrapper = None
  try:
    # Check if iasl is already installed
    if (path := which('iasl')):
      iasl = partial(wrap_binary, binary_path=path)
    # Otherwise, extract a temporary iasl binary
    elif not tmp_wrapper:
      with extract_iasl_binary(cache=True, persist=True) as tmp_wrapper:
        iasl = tmp_wrapper
    #TODO: Add option to provide -da or -e flag w/ user-provided DSDT/SSDTs
    # @see https://www.tonymacx86.com/threads/guide-patching-laptop-dsdt-ssdts.152573/
    # @see https://github.com/acpica/acpica/issues/414#issuecomment-432378819
    yield iasl
  finally:
    if tmp_wrapper:# and not cache:
      PathResolver(iasl.keywords['binary_path']).unlink()

@contextmanager
def translate_ssdts(filepaths: List[Union[str, PathResolver]],
                    directory: Optional[Union[str, PathResolver]]=None,
                    persist: bool=False
                    ) -> Generator[List[PathResolver], any, None]:
  """Decompiles or compiles SSDT tables using iasl.

  Args:
    filepaths: A list of filepaths to SSDT *.aml or *.dsl files.
    persist: Whether to persist the SSDT files.

  Yields:
    A list of filepaths to the compiled + decompiled SSDT files.
  """
  tmp_dir = PathResolver(mkdtemp(dir=directory))
  try:
    with iasl_wrapper() as iasl:
      for filepath in map(PathResolver, filepaths):
        tmp_copy = tmp_dir.joinpath(filepath.name)
        copyfile(filepath, tmp_copy)
        iasl(['-ve', tmp_copy])
    yield list(map(PathResolver, tmp_dir.iterdir()))
  finally:
    # Cleanup after context exits
    if not persist: rmtree(tmp_dir)

def sort_ssdt_symbols(filepaths: List[Union[str, PathResolver]]) -> OrderedDict:
  """Sorts the injection order of SSDT tables by resolving symbolic references.

  This is a naive implementation that does not prune conditional branches or
  build flags outside of standard ACPI spec.

  Args:
    filepaths: A list of filepaths to SSDT *.dsl files.

  Returns:
    An ordered dictionary of SSDT table names with their exported symbols.
  """
  ssdt_names = list(PathResolver(f).stem for f in filepaths)

  # Extract flat tree of SSDT symbols and tables
  dependency_tree = OrderedDict()
  for ssdt, filepath in sorted(zip(ssdt_names, filepaths)):
    with open(filepath, 'r', encoding='UTF-8') as file:
      namespace = parse_ssdt_namespace(file)
    dependency_tree[ssdt] = list(namespace['imports'].keys())
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
    elif table not in sorted_dependencies:
      sorted_dependencies[table] = []
    elif table not in ssdt_names:
      sorted_dependencies[table].append(symbol)

  # Sort table dependencies by root -> alphabetically
  for k, arr in sorted_dependencies.items():
    sorted_dependencies[k] = sorted(arr, key=lambda s: (s.count('.'), s))

  return sorted_dependencies

def extract_ssdts(directory: Union[str, PathResolver]) -> dict:
  """Extracts the metadata of all SSDTs in a directory."""
  ssdts = {}
  ssdt_paths = glob(directory, '**/*.aml', include='**/*.dsl')
  with translate_ssdts(ssdt_paths, directory, persist=True) as translated_ssdts:
    for ssdt_path in filter(lambda p: p.suffix == '.aml', translated_ssdts):
      extract_path = f'.{ssdt_path.as_posix().split(directory.as_posix())[1]}'
      source_path = PathResolver(str(ssdt_path).replace('.aml', '.dsl'))
      # Update ssdt dictionary
      ssdts[ssdt_path.stem] = {
        "__path": ssdt_path,
        "__extracted": extract_path,
        "source": source_path
      }

  return ssdts

__all__ = [
  # Functions (5)
  "extract_iasl_binary",
  "iasl_wrapper",
  "translate_ssdts",
  "sort_ssdt_symbols",
  "extract_ssdts"
]
