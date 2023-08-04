## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

from pathlib import PosixPath, PurePosixPath, PureWindowsPath, WindowsPath

from .pathlib import BasePath, Path, PurePath


def test_Path():
  args = 'foo/bar'
  instance = Path(args)
  flavours = (PosixPath, WindowsPath)

  assert instance.__class__ == Path
  assert instance.__getinstance__().__class__ in flavours
  assert repr(instance) == f"Path({repr(args)})"
  assert isinstance(instance, BasePath)

  # Test subclassing
  class CustomPath(Path):
    foo = 'bar'

  subclass_instance = CustomPath(args)

  assert subclass_instance.__class__ == CustomPath
  assert subclass_instance.__getinstance__().__class__ in flavours
  assert repr(subclass_instance) == f"CustomPath({repr(args)})"
  assert subclass_instance.foo == 'bar'
  assert isinstance(subclass_instance, BasePath)
  assert isinstance(subclass_instance, Path)

  # Test MRO cooperative subclassing
  assert subclass_instance.cls_flavour == instance.cls_flavour
  assert subclass_instance.subclasses == instance.subclasses
  assert instance.subclasses[-1] == subclass_instance.__class__

def test_PurePath():
  args = 'foo/bar'
  instance = PurePath(args)
  flavours = (PurePosixPath, PureWindowsPath)

  assert instance.__class__ == PurePath
  assert instance.__getinstance__().__class__ in flavours
  assert repr(instance) == f"PurePath({repr(args)})"
  assert isinstance(instance, BasePath)

  # Test subclassing
  class CustomPurePath(PurePath):
    foo = 'bar'

  subclass_instance = CustomPurePath(args)

  assert subclass_instance.__class__ == CustomPurePath
  assert subclass_instance.__getinstance__().__class__ in flavours
  assert repr(subclass_instance) == f"CustomPurePath({repr(args)})"
  assert subclass_instance.foo == 'bar'
  assert isinstance(subclass_instance, BasePath)
  assert isinstance(subclass_instance, PurePath)

  # Test MRO cooperative subclassing
  assert subclass_instance.cls_flavour == instance.cls_flavour
  assert subclass_instance.subclasses == instance.subclasses
  assert instance.subclasses[-1] == subclass_instance.__class__

  # Verify no pollution of the `pathlib` module by the Path class
  assert not hasattr(subclass_instance, 'resolve')
  assert not hasattr(instance, 'resolve')
