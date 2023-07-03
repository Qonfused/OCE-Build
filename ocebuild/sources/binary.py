#pragma no-implicit

## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Binary helper functions."""

from os import chmod
from platform import system
import subprocess

from typing import List, Literal

from ocebuild.errors._lib import disable_exception_traceback
from ocebuild.sources.resolver import PathResolver


def get_binary_ext(platform: Literal['Windows', 'Darwin', 'Linux']=system()
                   ) -> str:
  """Gets a platform-dependent extension for vendored binaries."""
  if   platform == 'Windows': return '.exe'
  elif platform == 'Darwin':  return ''
  elif platform == 'Linux':   return '.linux'

def wrap_binary(args: List[str], binary_path: str) -> str:
  """Wraps a binary and returns stdout."""
  if not isinstance(args, list): args = [args]
  chmod(binary_path := binary_path, 0o755)
  process = subprocess.run([binary_path, *args],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='UTF-8')
  # Raise error without stacktrace
  if process.returncode:
    with disable_exception_traceback():
      stderr_name = PathResolver(binary_path).name
      raise Exception(f'({stderr_name}) {process.stderr.strip()}')
  return process.stdout

__all__ = [
  # Functions (2)
  "get_binary_ext",
  "wrap_binary"
]
