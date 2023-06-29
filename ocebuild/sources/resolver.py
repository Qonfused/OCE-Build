## @file
# Custom specifier resolver classes and methods.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

from inspect import signature
from pathlib import Path
from typing import Any, Generator, Tuple, TypeVar

from sources.dortania import *
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

  @property
  def __parameters__(self: TBaseResolver) -> dict:
    """Returns a dict of publically accessible parameters."""
    return { k:v for k,v in self.__dict__.items()
             if not k.startswith('__') }

  def __iter__(self: TBaseResolver) -> Generator[Tuple[str, str], any, None]:
    """Returns only public parameters in `__iter__` calls."""
    for k,v in self.__parameters__.items():
      if v is not None: yield k,v

  def has_any(self: TBaseResolver,
              *parameters: Tuple[str, ...]
              ) -> bool:
    """Returns true if any of the specified parameters are present."""
    self_params = dict(self)
    return any(k in self_params for k in parameters
               if self_params.get(k) is not None)

class GitHubResolver(BaseResolver):
  """Resolves a GitHub URL based on the class parameters."""
  TGitHubResolver = TypeVar("TGitHubResolver", bound="GitHubResolver")

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
    # Instantiates internal resolver properties
    super().__init__(self, *args, **kwargs)

    # Public properties
    self.repository = repository
    self.path = path
    self.branch = branch
    self.tag = tag
    self.workflow = workflow
    self.commit = commit
  
  def resolve(self: TGitHubResolver) -> str:
    """Returns a URL based on the class parameters."""
    params = dict(self)
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

class DortaniaResolver(BaseResolver):
  """Resolves a Dortania build URL based on the class parameters."""
  TDortaniaResolver = TypeVar("TDortaniaResolver", bound="DortaniaResolver")

  def __init__(self: TDortaniaResolver,
               commit: Optional[str]=None,
               *args,
               **kwargs):
    # Ensure MRO is cooperative with subclassing
    super(DortaniaResolver, self).__init__()
    # Instantiates internal resolver properties
    super().__init__(self, *args, **kwargs)

    # Public properties
    self.commit = commit

  def resolve(self: TDortaniaResolver) -> str:
    """Returns a URL based on the class parameters."""
    plugin = self.__name__
    params = dict(self)
    # Resolve build commit sha
    commit_sha: str
    if self.has_any('commit'):
      commit_sha = params['commit']
    else:
      commit_sha = get_latest_sha(plugin)
    # Return the latest build (default) or by commit sha
    return dortania_release_url(plugin, commit=commit_sha)

class PathResolver(BaseResolver, cls := type(Path())):
  """Resolves a filepath based on the class parameters."""
  TPathResolver = TypeVar("TPathResolver", bound="PathResolver")

  def __init__(self: TPathResolver,
               path: Path,
               *args,
               **kwargs):
    # Ensure MRO is cooperative with subclassing
    super(PathResolver, self).__init__()
    # Instantiates internal resolver properties
    super().__init__(self, *args, **kwargs)

    # Public properties
    self.path = path

    # Attempt to subclass pathlib.Path directly - Python 3.12+
    # @see https://github.com/Qonfused/OCE-Build/pull/4#issuecomment-1611019621
    try:
      super(cls, self).__init__(path, *args)
    # Instantiates a new Path subclass using the `__new__` method.
    except:
      self.__cls__ = super().__new__(cls, path, *args, **kwargs)
  
  def __getattribute__(self: TPathResolver, name: str) -> Any:
    """Retrieves from the instantiated class or subclass."""
    self_attr = super().__getattribute__(name)
    try:
      # Get the uninstantiated class representation
      class_repr = super().__getattribute__('__class__')
      # Get the instantiated subclass attribute (if either exists)
      cls_ref = super().__getattribute__('__cls__')
      cls_attr = cls_ref.__getattribute__(name)
      # Only return attribute if not overridden
      assert not class_repr.__getattribute__(name)
      assert signature(self_attr) == signature(cls_attr)
      # Return class attribute
      return cls_attr
    # Return the class attribute (if it exists)
    except:
      return self_attr
  
  def resolve(self: TPathResolver, strict: bool = False) -> cls:
    """Returns a filepath based on the class parameters."""
    resolved_path: cls
    # Check if path has called the `__init__` method - Python 3.12+
    if '_raw_paths' in dir(self):
      resolved_path = super(cls, self).resolve(strict)
    # Fall back to calling initialized `__cls__` subclass
    elif '__cls__' in dir(self):
      resolved_path = self.__cls__.resolve(strict)
    # Fall back to initializing and calling a new cls subclass
    else:
      resolved_path = cls(self.path).resolve()
    
    #TODO: Handle additional path type verifications here
    return resolved_path
