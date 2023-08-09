## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Methods for retrieving and handling SSDT binaries and source code."""

from collections import OrderedDict
from contextlib import contextmanager
from functools import partial
from graphlib import TopologicalSorter
from os import makedirs, SEEK_END
from shutil import copyfile, rmtree, which
from tempfile import mkdtemp, NamedTemporaryFile

from typing import Callable, Generator, List, Optional, Union

from ocebuild.filesystem import glob, remove
from ocebuild.filesystem.cache import CACHE_DIR, UNPACK_DIR
from ocebuild.parsers.asl import parse_ssdt_namespace
from ocebuild.sources import request
from ocebuild.sources.binary import get_binary_ext, wrap_binary
from ocebuild.sources.github import github_file_url

from third_party.cpython.pathlib import Path


@contextmanager
def extract_iasl_binary(url: Optional[str]=None,
                        cache: bool=True,
                        persist: bool=False
                        ) -> Generator[Callable[[List[str]], str], any, None]:
  """Extracts an iasl binary and yields a subprocess wrapper.

  Args:
    url: The URL to the iasl binary. If not provided, the URL will be
        automatically retrieved based on the current platform.
    cache: Whether to cache the extracted iasl binary for subsequent calls.
    persist: Whether to persist the binary wrapper outside the current context.

  Yields:
    A subprocess wrapper for the extracted iasl binary.
  """
  binary = f'iasl{get_binary_ext()}'
  extract_dir = CACHE_DIR.joinpath('iasl')
  try:
    # Create a temporary file to store the iasl binary
    makedirs(extract_dir, exist_ok=True)
    if cache:
      filepath = extract_dir.joinpath(binary)
      mode = 'w+b' if not filepath.exists() else 'r+b'
      file = open(extract_dir.joinpath(binary), mode)
    else:
      file = NamedTemporaryFile(suffix=f'-{binary}', dir=extract_dir)
    file.seek(0, SEEK_END)
    # Download the iasl binary if the file is empty
    if not file.tell():
      # Fetch the iasl binary appropriate for the current platform
      if not url:
        url = github_file_url('Qonfused/iASL', path=binary, raw=True)
      # Fetch and extract the iasl binary to a temporary file
      with request(url) as response:
        file.seek(0)
        file.write(response.read())
        file.close()
    # Yield a wrapper over the iasl binary
    yield partial(wrap_binary, binary_path=file.name)
  finally:
    # Cleanup after context exits
    if not persist: remove(extract_dir)

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
      with extract_iasl_binary(cache=cache, persist=True) as tmp_wrapper:
        iasl = tmp_wrapper
    #TODO: Add option to provide -da or -e flag w/ user-provided DSDT/SSDTs
    # @see https://www.tonymacx86.com/threads/guide-patching-laptop-dsdt-ssdts.152573/
    # @see https://github.com/acpica/acpica/issues/414#issuecomment-432378819
    yield iasl
  finally:
    if tmp_wrapper and not cache:
      remove(iasl.keywords['binary_path'])

@contextmanager
def translate_ssdts(filepaths: List[Union[str, Path]],
                    directory: Optional[Union[str, Path]]=None,
                    persist: bool=False
                    ) -> Generator[List[Path], any, None]:
  """Decompiles or compiles SSDT tables using iasl.

  Args:
    filepaths: A list of filepaths to SSDT *.aml or *.dsl files.
    persist: Whether to persist the SSDT files.

  Yields:
    A list of filepaths to the compiled + decompiled SSDT files.
  """
  tmp_dir = Path(mkdtemp(dir=directory))
  try:
    with iasl_wrapper() as iasl:
      for filepath in map(Path, filepaths):
        tmp_copy = tmp_dir.joinpath(filepath.name)
        copyfile(filepath, tmp_copy)
        iasl(['-ve', tmp_copy])
    yield list(map(Path, tmp_dir.iterdir()))
  finally:
    # Cleanup after context exits
    if not persist: rmtree(tmp_dir)

def sort_ssdt_symbols(filepaths: List[Union[str, Path]]) -> OrderedDict:
  """Sorts the injection order of SSDT tables by resolving symbolic references.

  This is a naive implementation that does not prune conditional branches or
  build flags outside of standard ACPI spec. It is intended to be used as a
  baseline reference for the injection order of SSDT tables in the absence of
  information about the system's DSDT.

  Args:
    filepaths: A list of filepaths to SSDT *.dsl files.

  Returns:
    An ordered dictionary of SSDT table names with their exported symbols.
  """
  ssdt_names = list(Path(f).stem for f in filepaths)

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

def extract_ssdts(directory: Union[str, Path], persist: bool=False) -> dict:
  """Extracts the metadata of all SSDTs in a directory."""
  ssdts = {}
  ssdt_paths = glob(directory, '**/*.aml', include='**/*.dsl')
  with translate_ssdts(ssdt_paths, UNPACK_DIR, persist=True) as translated_ssdts:
    for ssdt_path in filter(lambda p: p.suffix == '.aml', translated_ssdts):
      name = ssdt_path.stem
      source_path = next(filter(lambda p: p.stem == name, ssdt_paths))
      relative = f'.{source_path.as_posix().split(directory.as_posix())[1]}'
      # Update ssdt dictionary
      ssdts[name] = {
        "__extracted": ssdt_path,
        "__path": relative
      }
      # Cleanup
      source_path = Path(str(ssdt_path).replace('.aml', '.dsl'))
      if not persist:
        remove(source_path)
      else:
        ssdts[name]["source"] = source_path

  return ssdts


__all__ = [
  # Functions (5)
  "extract_iasl_binary",
  "iasl_wrapper",
  "translate_ssdts",
  "sort_ssdt_symbols",
  "extract_ssdts"
]
