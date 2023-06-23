## @file
# Methods for handling cross-platform file system operations.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

from os import PathLike
from pathlib import Path
from shutil import move as shutil_move


def move(src: str | PathLike[str],
         target: str | PathLike[str]):
  """Moves a file or directory to a new location.

  This is a simple wrapper over shutil's `move` method that
  recursively creates missing directories in the target path.

  Args:
    src: Source path.
    target: Destination path.

  Returns:
    The destination path.
  """
  dest = Path(target, Path(src).name)
  if not (parent_dir := dest.parent).is_dir() and str(parent_dir) != '.':
    parent_dir.mkdir(parents=True, exist_ok=True)
  return shutil_move(src, parent_dir)

def glob(directory: str | PathLike[str],
         pattern: str,
         first: bool = False) -> list[Path] | Path | None:
  """Returns a list of paths matching the given pattern.

  Args:
    directory: Directory to search.
    pattern: Glob pattern.
    first: Whether to return only the first match.

  Returns:
    A list of matching paths.
    Instead returns the first matching path if `first` is `True`.
    Returns `None` if no matches are found.
  """
  matches = list(Path(directory).glob(pattern))
  if len(matches):
    return matches if not first else matches[0]
  return None
