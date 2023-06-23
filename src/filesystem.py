## @file
# Methods for handling cross-platform file system operations.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

from os import rename as os_rename, PathLike
from pathlib import Path
from shutil import move as shutil_move

from typing import Optional


def rename(path: str | PathLike[str],
           name: str) -> Path:
  """Renames a file or directory.

  Args:
    path: Path to the file or directory.
    name: New name for the file or directory.
  
  Returns:
    The renamed path.
    
  Raises:
    FileNotFoundError: If the file or directory does not exist.
    OSError: If the file or directory cannot be renamed.
  """
  parent_dir = Path(path).parent
  output_dir = Path(parent_dir, name)
  os_rename(path, output_dir)
  return output_dir

def move(src: str | PathLike[str],
         target: str | PathLike[str],
         name: Optional[str]=None) -> Path:
  """Moves a file or directory to a new location.

  This is a simple wrapper over shutil's `move` method that
  recursively creates missing directories in the target path.

  Args:
    src: Source path.
    target: Destination path.
    name (Optional): Destination file or directory name.

  Returns:
    The destination path.
  """
  dest = Path(target, name if name else Path(src).name)
  if not (parent_dir := dest.parent).is_dir() and str(parent_dir) != '.':
    parent_dir.mkdir(parents=True, exist_ok=True)
  shutil_move(src, parent_dir if not name else dest)
  return dest

def glob(directory: str | PathLike[str],
         pattern: str,
         first: bool = False) -> list[Path] | Path:
  """Returns a list of paths matching the given pattern.

  Args:
    directory: Directory to search.
    pattern: Glob pattern.
    first (Optional): Whether to return only the first match.

  Returns:
    A list of matching paths.
    Instead returns the first matching path if `first` is `True`.
  """
  matches = list(Path(directory).glob(pattern))
  return matches[0] if first and len(matches) else matches
