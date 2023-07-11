## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Methods for handling cross-platform file system operations."""

from os import PathLike, rename as os_rename
from shutil import move as shutil_move, rmtree

from typing import Generator, List, Optional, Union

from ocebuild.sources.resolver import PathResolver


def remove(path: Union[str, "PathLike[str]"]) -> None:
  """Removes a file or directory."""
  path = PathResolver(path)
  if not path.exists(): return
  elif path.is_file(): path.unlink()
  elif path.is_dir(): rmtree(path)
  else:
    raise ValueError(f'Path is not a file or directory: {path}')


def rename(path: Union[str, "PathLike[str]"],
           name: str
           ) -> PathResolver:
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
  parent_dir = PathResolver(path).parent
  output_dir = PathResolver(parent_dir, name)
  os_rename(path, output_dir)
  return output_dir

def move(src: Union[str, "PathLike[str]"],
         target: Union[str, "PathLike[str]"],
         name: Optional[str]=None
         ) -> PathResolver:
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
  dest = PathResolver(target, name if name else PathResolver(src).name)
  if not (parent_dir := dest.parent).is_dir() and str(parent_dir) != '.':
    parent_dir.mkdir(parents=True, exist_ok=True)
  shutil_move(str(src), parent_dir if not name else dest)
  return dest

def glob(directory: Union[str, "PathLike[str]"],
         pattern: str,
         include: Optional[Union[str, List[str]]]=None,
         exclude: Optional[Union[str, List[str]]]=None,
         first: Optional[bool] = False
         ) -> Union[Generator[PathResolver, None, None], PathResolver, None]:
  """Returns a list of paths matching the given pattern.

  Args:
    directory: Directory to search.
    pattern: Glob pattern.
    include: A glob pattern or list of glob patterns to include.
    exclude: A glob pattern or list of glob patterns to exclude.
    first (Optional): Whether to return only the first match.

  Returns:
    A list of matching paths.
    Instead returns the first matching path if `first` is `True`.
  """
  matches = list(PathResolver(directory).glob(pattern))
  if include is not None:
    if isinstance(include, str): include = [include]
    include_matches = set()
    for s in include:
      include_matches |= set(PathResolver(directory).glob(s))
    matches = list((*set(matches), *include_matches))
  if exclude is not None:
    if isinstance(exclude, str): exclude = [exclude]
    exclude_matches = set()
    for s in exclude:
      exclude_matches |= set(PathResolver(directory).glob(s))
    matches = list(set(matches) - exclude_matches)
  if first:
    return matches[0] if len(matches) else None
  return matches


__all__ = [
  # Functions (4)
  "remove",
  "rename",
  "move",
  "glob"
]
