#pragma no-implicit

## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Binary helper functions."""

import subprocess
from hashlib import sha256
from os import chmod, walk
from platform import system

from typing import List, Literal

from .resolver import PathResolver

from ocebuild.errors._lib import disable_exception_traceback


def get_binary_ext(platform: Literal['Windows', 'Darwin', 'Linux']=system()
                   ) -> str:
  """Gets a platform-dependent extension for vendored binaries."""
  if   platform == 'Windows': return '.exe'
  elif platform == 'Darwin':  return ''
  elif platform == 'Linux':   return '.linux'

def _get_file_digest(filename, hash) -> str:
  """Gets a digest for a file."""
  with open(filename, 'rb') as file:
    while True:
      chunk = file.read(hash.block_size)
      if not chunk: break
      hash.update(chunk)
  return hash

def _get_dir_digest(directory, hash):
  """Recursively gets a digest for all files in a directory."""
  for path in sorted(PathResolver(directory).iterdir()):
    # Ensure subdirectories are sorted for consistent hashes
    hash.update(path.name.encode())
    if path.is_file():
      hash = _get_file_digest(path, hash)
    elif path.is_dir():
      hash = _get_dir_digest(path, hash)
  return hash

def get_digest(filepath, algorithm=sha256) -> str:
  """Gets a digest for a file or directory.
  
  Args:
    filepath: The path to the file or directory.
    algorithm: The hashlib algorithm method to use.
  
  Returns:
    A hex digest of the file or directory.
  """
  hash = algorithm()
  if not (path := PathResolver(filepath)).exists():
    raise FileNotFoundError(f'No such file or directory: {filepath}')
  elif path.is_file():
    _get_file_digest(filepath, hash)
  elif path.is_dir():
    _get_dir_digest(filepath, hash)

  return hash.digest().hex()

def wrap_binary(args: List[str], binary_path: str) -> str:
  """Wraps a binary and returns stdout.
  
  Args:
    args: The arguments to pass to the binary.
    binary_path: The path to the binary.

  Raises:
    Exception: If the binary returns a non-zero exit code.

  Returns:
    The stdout of the binary.
  """
  if not isinstance(args, list): args = [args]
  chmod(binary_path := binary_path, 0o755)
  process = subprocess.run([binary_path, *args],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='UTF-8')
  # Raise error without stacktrace
  if process.returncode: #pragma: no cover
    with disable_exception_traceback():
      stderr_name = PathResolver(binary_path).name
      raise Exception(f'({stderr_name}) {process.stderr.strip()}')
  return process.stdout

__all__ = [
  # Functions (3)
  "get_binary_ext",
  "get_digest",
  "wrap_binary"
]
