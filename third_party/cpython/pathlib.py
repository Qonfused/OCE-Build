#pragma preserve-exports

## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Overrides the `pathlib` module to support backports and custom subclasses."""

#pylint: disable=C0103,E0602,E1003,R1725,W0718

import pathlib
from inspect import signature
from pathlib import PosixPath, PurePosixPath, PureWindowsPath, WindowsPath

from typing import Any, List, Optional, TypeVar, Union

from .. import inject_module_namespace


class BasePath():
  """Provides a `pathlib` wrapper class that can be subclassed idiomatically."""

  TBasePath = TypeVar("TBasePath", bound="BasePath")
  """BasePath class type alias for overriding built-in method signatures.
  @internal
  """

  cls_flavour: TBasePath
  subclasses: List[TBasePath] = []

  def __init__(self: TBasePath, *args, **kwargs):
    # Ensure MRO is cooperative with subclassing
    super(BasePath, self).__init__()

    # Attempt to subclass pathlib.Path directly - Python 3.12+
    # @see https://github.com/Qonfused/OCE-Build/pull/4#issuecomment-1611019621
    try:
      super(self.cls_flavour, self).__init__(*args)
    # Instantiates a new Path subclass using the `__new__` method.
    # This uses a __cls__ hook as a fallback for the `__getattribute__` method.
    except Exception: #pragma: no cover
      self.__cls__ = super().__new__(self.cls_flavour, *args, **kwargs)

  @classmethod
  def __init_subclass__(cls: TBasePath,
                        /,
                        as_flavour: Optional[any]=None,
                        **kwargs):
    """Initializes a new subclass of a `pathlib` module baseclass.

    Args:
      cls: The subclass to initialize.
      as_flavour: The `pathlib` flavour class to subclass.
      **kwargs: Additional keyword arguments to pass to the superclass.
    """

    super().__init_subclass__(**kwargs)

    # If specified, override the Path/PurePath flavour subclass
    if as_flavour:
      cls.cls_flavour = as_flavour
    # Otherwise append Path/PurePath subclasses
    elif cls.__bases__[0] != BasePath:
      cls.subclasses.append(cls)

  def __getattribute__(self: TBasePath, __name: str) -> Any:
    """Retrieves an attribute from the instantiated class or subclass."""
    self_attr = super().__getattribute__(__name)

    # Attempt to retrieve overridden class attributes
    try: #pragma: no cover
      # Get the uninstantiated class representation
      class_repr = super().__getattribute__('__class__')

      # Get the instantiated subclass attribute (if either exists)
      cls_ref = super().__getattribute__('__cls__')
      cls_attr = cls_ref.__getattribute__(__name)

      # Only return attribute if not overridden
      assert not class_repr().__getattribute__(__name)
      assert signature(self_attr) == signature(cls_attr)

      # Otherwise return the class attribute
      return cls_attr
    except Exception: #pragma: no cover
      pass

    # Fallback to the class attribute (if it exists)
    return self_attr

  def __getinstance__(self: TBasePath) -> TBasePath:
    """Retrieves the currently instantiated concrete path baseclass."""
    cls_instance: self.cls_flavour
    try: #pragma: no cover
      # Check if `pathlib.Path` has called the `__init__` method - Python 3.12+
      if '_raw_paths' in dir(self):
        cls_instance = super(self.cls_flavour, self)
      # Fall back to calling initialized `__cls__` subclass
      elif '__cls__' in dir(self):
        cls_instance = self.__cls__
      # Fall back to initializing and calling a new path flavour subclass
      else:
        cls_instance = self.cls_flavour(self)
    except Exception as e: #pragma: no cover
      raise RuntimeError("Unable to retrieve instantiated path class.") from e

    return cls_instance

class Path(BasePath, Path_flavour := type(pathlib.Path())):
  """Provides a `pathlib.Path` class that can be subclassed idiomatically."""

  TPath = TypeVar("TPath", bound="Path")
  """Path class type alias for overriding built-in method signatures.
  @internal
  """

  cls_flavour = Path_flavour
  subclasses: List[TPath] = []

  def relative(self: TPath,
               path: Union[str, TPath]='.',
               from_parent: bool=False
               ) -> str:
    """Resolves a relative representation from a file or directory path."""
    parent_dir = Path(path).resolve()
    if from_parent and self.resolve().is_file():
      parent_dir = parent_dir.parent
    return self.resolve().relative_to(parent_dir).as_posix()

class PurePath(BasePath, PurePath_flavour := type(pathlib.PurePath())):
  """Provides a `pathlib.PurePath` class that can be subclassed idiomatically."""

  TPurePath = TypeVar("TPurePath", bound="PurePath")
  """PurePath class type alias for overriding built-in method signatures.
  @internal
  """

  cls_flavour = PurePath_flavour
  subclasses: List[TPurePath] = []


# Inject the `pathlib` namespace into the current module
inject_module_namespace(pathlib, namespace=globals())

__all__ = [
  "Path",
  "PurePath",
  "PosixPath",
  "PurePosixPath",
  "WindowsPath",
  "PureWindowsPath"
]
