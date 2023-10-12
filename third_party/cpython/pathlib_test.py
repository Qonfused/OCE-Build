## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

from pathlib import PosixPath, PurePosixPath, PureWindowsPath, WindowsPath

from .pathlib import BasePath, Path, PurePath


def assert_mro_cooperative_subclassing(derived, args, instance, flavours):
  """Asserts that the provided instance is a subclass of the appropriate flavour.

  Args:
    instance: The class instance to test.
    derived: The derived class that the instance should be an instance of.
    args: The arguments used to instantiate the instance.
    flavours: The flavours/variants that the instance should be a subclass of.

  Raises:
    AssertionError: If the instance is not a subclass of the appropriate flavour.
  """
  # This performs the same test for asserting that __class__ proxy object
  # provided by the PurePath class is a subclass of the appropriate flavour
  cls = next(c for c in type(instance).mro() if not 'third_party' in str(c))
  if flavours:
    assert cls in flavours
    assert isinstance(instance, cls)
    assert type(instance).__mro__.index(cls) == len(derived)
  # Derives from vendored class (e.g. PurePath) and the BasePath class
  for mro_cls in derived:
    assert mro_cls in type(instance).__mro__
    assert isinstance(instance, mro_cls)
    assert type(instance).__mro__.index(mro_cls) == derived.index(mro_cls)
  assert repr(instance) == f"{derived[0].__name__}({repr(args)})"
  # Verify that the __class__ proxy is a subclass of the appropriate flavour


def test_Path():
  args = 'foo/bar'
  instance = Path(args)
  flavours = (PosixPath, WindowsPath)
  assert_mro_cooperative_subclassing((Path, BasePath),
                                     args, instance, flavours)

  # Test subclassing
  class CustomPath(Path):
    foo = 'bar'

  subclass_instance = CustomPath(args)

  assert_mro_cooperative_subclassing((CustomPath, Path, BasePath),
                                     args, subclass_instance, flavours)

  # Test MRO cooperative subclassing
  assert subclass_instance.cls_flavour == instance.cls_flavour
  assert subclass_instance.subclasses == instance.subclasses
  assert instance.subclasses[-1] == subclass_instance.__class__

def test_PurePath():
  args = 'foo/bar'
  instance = PurePath(args)
  flavours = (PurePosixPath, PureWindowsPath)
  assert_mro_cooperative_subclassing((PurePath, BasePath),
                                     args, instance, flavours)

  # Test subclassing
  class CustomPurePath(PurePath):
    foo = 'bar'

  subclass_instance = CustomPurePath(args)
  assert_mro_cooperative_subclassing((CustomPurePath, PurePath, BasePath),
                                     args, subclass_instance, flavours)

  # Test MRO cooperative subclassing
  assert subclass_instance.cls_flavour == instance.cls_flavour
  assert subclass_instance.subclasses == instance.subclasses
  assert instance.subclasses[-1] == subclass_instance.__class__

  # Verify no pollution of the `pathlib` module by the Path class
  assert not hasattr(subclass_instance, 'resolve')
  assert not hasattr(instance, 'resolve')
