#pragma no-implicit

## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Validation methods used for testing and at runtime."""

#pylint: disable=cell-var-from-loop

from contextlib import suppress
from functools import partial
from os import PathLike

from typing import Callable, Literal, Optional, Tuple, Union

from ._lib import disable_exception_traceback
from .types import PathValidationError

from ocebuild.parsers.dict import flatten_dict

from third_party.cpython.pathlib import Path


def validate(call: Callable[[], bool],
             err: Union[Exception, Callable[[Tuple[any, ...]], Exception]],
             msg: Optional[str]
             ) -> None:
  """Throws a ValidationError with the given message."""
  result: bool=True
  # Override AssertionError context with ValidationError
  with suppress(AssertionError): result=call()
  if not result:
    with disable_exception_traceback():
      raise err(msg if msg else f'Failed {call.__name__} validation test')

def validate_path_tree(path: Union[str, "PathLike[str]"],
                       tree: dict,
                       delimiter: str='/'
                       ) -> Literal[True]:
  """Validates a given path matches a tree schema.

  Args:
    path: The path to validate.
    tree: The tree schema to validate against.
    delimiter: The delimiter to use when flattening the tree.

  Raises:
    PathValidationError: If the path does not match the tree schema.

  Returns:
    True if the path matches the tree schema.
  """
  # Verify path exists
  root_dir = Path(path)
  for ftree, flag in flatten_dict(tree, delimiter).items():
    # Create error partial for re-use
    absolute_path = root_dir.joinpath(*ftree.split('/'))
    name = absolute_path.name
    path = str(absolute_path)[len(str(root_dir))+1:]
    kind = 'file' if flag in ('f', 'file') else 'directory'
    err = partial(PathValidationError, name=name, kind=kind, path=path)
    # Verify path exists
    def path_exists() -> bool:
      return absolute_path.exists()
    validate(path_exists, err, msg=f"Missing {kind} '{name}' (at {path})")
    # Handle flags
    if flag == '*':
      # Verify subdirectory is populated
      def is_populated() -> bool:
        return bool(set(absolute_path.iterdir()))
      validate(is_populated, err, msg=f"Path '{name}' is empty (at {path})")
    elif flag in ('f', 'file', 'd', 'dir'):
      # Verify path type matches flag
      def is_type() -> bool:
        if kind == 'file':
          # Verify path points to a file
          return absolute_path.is_file()
        elif kind == 'directory':
          # Verify path points to a directory
          return absolute_path.is_dir()
        else:
          raise ValueError('Invalid path type given')
      validate(is_type, err, msg=f"Path '{name}' not a {kind} (at {path})")
    # Invalid flag
    else:
      raise ValueError(f"Invalid flag '{flag}' given for path '{name}' (at {path})")

  return True


__all__ = [
  # Functions (2)
  "validate",
  "validate_path_tree"
]
