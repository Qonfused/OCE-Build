## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

import pytest

from pathlib import Path
from typing import TypeVar

from sources.resolver import *


def test_BaseResolver():
  # Test `pathlib.Path` subclassing as a non-trivial use case
  class TestClass(BaseResolver, cls := type(Path())):
    """Resolves a filepath based on the class parameters."""
    TTestClass = TypeVar("TTestClass", bound="TestClass")

    def __init__(self: TTestClass,
                path: Path,
                *args,
                **kwargs):
      # Ensure MRO is cooperative with subclassing
      super(TestClass, self).__init__()
      # Public properties
      self.path = path
      # Instantiates internal resolver properties
      super().__init__(self, *args, **kwargs)
      # Instantiates a new Path subclass using the `__new__` method.
      self.__cls__ = super().__new__(cls, path, *args, **kwargs)

    def resolve(self: TTestClass,
                return_foo: Optional[bool]=None
                ) -> TTestClass:
      """Returns a filepath based on the class parameters."""
      if return_foo: return 'foo'
      resolved_path = self.__cls__.resolve()
      return resolved_path

  path = 'example/build.lock'
  output = TestClass(path, __name__='foo')
  # Validate BaseResolver props and methods
  assert output.__name__ == 'foo'
  assert dict(output) == dict(path=path)
  # Validate pathlib.Path props and methods
  # assert repr(output.resolve()) == repr(Path(path).resolve())
  assert output.resolve()
  assert output.stem == Path(path).stem
  # Validate TestClass props and methods
  assert output.resolve(return_foo=True) == 'foo'
  assert output.path == path

def test_GitHubResolver():
  # Test release url resolution
  assert GitHubResolver(repository='acidanthera/RestrictEvents',
                        tag='~1.0.6'
                        ).resolve() == \
    'https://github.com/acidanthera/RestrictEvents/releases/tag/1.0.9'
  # Test raw file url resolution
  assert GitHubResolver(repository='acidanthera/RestrictEvents',
                        branch='force-vmm-install',
                        path='RestrictEvents/Info.plist'
                        ).resolve() == \
    'https://raw.githubusercontent.com/acidanthera/RestrictEvents/force-vmm-install/RestrictEvents/Info.plist'
  # Test artifact url resolution
  assert GitHubResolver(repository='acidanthera/RestrictEvents',
                        branch='force-vmm-install',
                        commit='e5c52564f5bca1aebbd916f2753f5a58809703a8'
                        ).resolve() == \
    'https://github.com/acidanthera/RestrictEvents/suites/13511383482/artifacts/742567994'
  # Test latest release url resolution
  assert GitHubResolver(repository='acidanthera/RestrictEvents').resolve()

def test_PathResolver():
  # Test relative filepath resolutions
  assert PathResolver('example/build.lock').resolve() == \
    Path('example/build.lock').resolve()
  assert PathResolver('ocebuild/../example/build.lock').resolve() == \
    Path('example/build.lock').resolve()
