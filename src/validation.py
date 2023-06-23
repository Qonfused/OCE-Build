## @file
# Validation methods used for testing and at runtime.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

from contextlib import suppress
from functools import partial
from os import PathLike
from pathlib import Path

from typing import Callable, Literal

from parsers.dict import flatten_dict


def validate(call: Callable[[], bool],
             err: Exception | partial[Exception]=Exception,
             msg: str='Failed {} validation test'):
  """Throws a ValidationError with the given message."""
  result: bool=True
  # Override AssertionError context with ValidationError
  with suppress(AssertionError):
    result: bool=call()
  if not result:
    raise err(msg.format(call.__name__))

class PathValidationError(Exception):
  def __init__(self,
               message: str,
               name: str,
               path: str,
               kind: str):
    super().__init__(message)
    self.name = name
    self.path = path
    self.kind = kind

def validate_path_tree(path: str | PathLike[str],
                       tree: dict,
                       delimiter: str='/') -> Literal[True]:
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
  for tree, flag in flatten_dict(tree, delimiter).items():
    # Create error partial for re-use
    with root_dir.joinpath(*tree.split('/')) as absolute_path:
      name = absolute_path.name
      path = str(absolute_path)[len(str(root_dir))+1:]
      kind = 'file' if flag == 'f' or flag == 'file' else 'directory'
      err = partial(PathValidationError, name=name, kind=kind, path=path)
    # Verify path exists
    def path_exists():
      return absolute_path.exists()
    validate(path_exists, err, msg=f"Missing {kind} '{name}' (at {path})")
    # Handle flags
    match flag:
      # Verify subdirectory is populated
      case '*':
        def is_populated():
          return len(set(absolute_path.iterdir()))
        validate(is_populated, err, msg=f"Path '{name}' is empty (at {path})")
      # Verify path type
      case 'f' | 'file' | 'd' | 'dir':
        def is_type():
          match kind:
            # Verify path points to a file
            case 'file':
              return absolute_path.is_file()
            # Verify path points to a directory
            case 'directory':
              return absolute_path.is_dir()
        validate(is_type, err, msg=f"Path '{name}' not a {kind} (at {path})")
      # Invalid flag
      case _:
        raise ValueError(f"Invalid flag '{flag}' given for path '{name}' (at {path})")
  return True
