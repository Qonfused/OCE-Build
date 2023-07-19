## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Methods for handling cross-platform file caching operations."""

from tempfile import mkdtemp

from typing import Generator, Union

from .posix import remove

from ocebuild.sources.resolver import PathResolver


def _iter_temp_dir(prefix: str,
                   dir_: Union[str, PathResolver]
                   ) -> Generator[PathResolver, any, None]:
  """Iterate over all temporary directories."""
  for d in PathResolver(dir_).iterdir():
    if d.is_dir() and d.name.startswith(prefix):
      yield d

def _get_temp_dir(prefix: str="ocebuild-cache-") -> PathResolver:
  """Return the path to a directory that can be used for ephemeral caching."""
  tmpdir = mkdtemp(prefix=prefix)
  cache_dirs = sorted(set(_iter_temp_dir(prefix, PathResolver(tmpdir).parent)),
                      key=lambda d: d.stat().st_ctime)
  # Remove all but the most recent cache directory
  for i,d in enumerate(cache_dirs):
    if i: remove(d)
  # Return the most recent cache directory
  return PathResolver(next(iter(cache_dirs), tmpdir))

UNPACK_DIR = _get_temp_dir(prefix="ocebuild-unpack-")
"""Directory for unpacking and handling remote or cached archives."""


__all__ = [
  # Constants (1)
  "UNPACK_DIR"
]
