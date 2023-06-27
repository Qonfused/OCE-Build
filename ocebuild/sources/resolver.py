## @file
# Custom specifier resolver classes and methods.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

from inspect import signature
from pathlib import Path

from typing import Any, Generator, Tuple, TypeVar

from sources.github import *
from versioning.semver import resolve_version_specifier


class BaseResolver():
  """Base resolver class implementing overrides."""
  TBaseResolver = TypeVar("TBaseResolver", bound="BaseResolver")

  def __init__(self: TBaseResolver,
               *args,
               __name__: Optional[str]=None,
               __specifier__: Optional[str]=None,
               **kwargs):
    # Ensure MRO is cooperative with subclassing
    super(BaseResolver, self).__init__()

    # Internal resolver properties
    self.__name__ = __name__
    self.__specifier__ = __specifier__

  def __getattribute__(self: TBaseResolver, name: str) -> Any:
    """Retrieves from the instantiated class or subclass."""
    self_attr = super().__getattribute__(name)
    try:
      # Return the instantiated subclass attribute (if either exists)
      with super().__getattribute__('__cls__') as cls_ref:
        cls_attr = cls_ref.__getattribute__(name)
        # Only return attribute if not overridden
        assert signature(self_attr) == signature(cls_attr)
        return cls_attr
    # Return the class attribute (if either exists)
    except:
      return self_attr

  @property
  def __parameters__(self: TBaseResolver) -> dict:
    """Returns a dict of publically accessible parameters."""
    return { k:v for k,v in self.__dict__.items()
             if not k.startswith('__') }

  def __iter__(self: TBaseResolver) -> Generator[Tuple[str, str], any, None]:
    """Returns only public parameters in `__iter__` calls."""
    for k,v in self.__parameters__.items():
      if v is not None: yield k,v

  def __str__(self: TBaseResolver) -> str:
    """Aliases `__str__` calls to `resolve()` for convenience."""
    return str(self.resolve())

  def has_any(self: TBaseResolver,
              *parameters: Tuple[str, ...]
              ) -> bool:
    """Returns true if any of the specified parameters are present."""
    self_params = dict(self)
    return any(k in self_params for k in parameters
               if self_params.get(k) is not None)

class GitHubResolver(BaseResolver):
  """Resolves a GitHub URL based on the class parameters."""
  TGitHubResolver= TypeVar("TGitHubResolver", bound="GitHubResolver")

  def __init__(self: TGitHubResolver,
               repository: str,
               path: Optional[str]=None,
               branch: Optional[str]=None,
               tag: Optional[str]=None,
               workflow: Optional[str]=None,
               commit: Optional[str]=None,
               *args,
               **kwargs):
    # Ensure MRO is cooperative with subclassing
    super(GitHubResolver, self).__init__()

    # Public properties
    self.repository = repository
    self.path = path
    self.branch = branch
    self.tag = tag
    self.workflow = workflow
    self.commit = commit

    # Instantiates internal resolver properties
    super().__init__(self, *args, **kwargs)
  
  def resolve(self: TGitHubResolver) -> str:
    """Returns a URL based on the class parameters."""
    params=dict(self)
    # Resolve version tag
    if self.has_any('tag'):
      tags = github_tag_names(repository=params['repository'])
      params['tag'] = resolve_version_specifier(versions=tags,
                                                specifier=params['tag'])
    # Return raw file url
    if self.has_any('path'):
      return github_file_url(**params, raw=True)
    # Resolve artifact from latest workflow run
    if self.has_any('branch', 'workflow', 'commit'):
      return github_artifacts_url(**params)
    # Return the latest release (default) or by tag
    return github_release_url(**params)

class PathResolver(BaseResolver, cls := type(Path())):
  """Resolves a filepath based on the class parameters."""
  TPathResolver = TypeVar("TPathResolver", bound="PathResolver")

  def __init__(self: TPathResolver,
               path: Path,
               *args,
               **kwargs):
    # Ensure MRO is cooperative with subclassing
    super(PathResolver, self).__init__()

    # Public properties
    self.path = path

    # Instantiates internal resolver properties
    super().__init__(self, *args, **kwargs)
    # Instantiates a new Path subclass using the `__new__` method.
    self.__cls__ = super().__new__(cls, path, *args, **kwargs)

  def resolve(self: TPathResolver) -> TPathResolver:
    """Returns a filepath based on the class parameters."""
    print('side effect')
    resolved_path = self.__cls__.resolve()
    #TODO: Handle additional path type verifications here
    return resolved_path
