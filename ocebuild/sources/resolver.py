## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Custom specifier resolver classes and methods."""

from difflib import get_close_matches
from inspect import signature
from pathlib import Path
from re import split

from typing import Any, Generator, List, Literal, Optional, Tuple, TypeVar, Union

from ocebuild.sources.dortania import *
from ocebuild.sources.github import *
from ocebuild.versioning.semver import resolve_version_specifier


class BaseResolver():
  """Base resolver class implementing overrides.

  This class is used to store custom specifier methods and metadata.
  @internal
  """
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
  
  @staticmethod
  def extract_asset(name: str,
                    url: str,
                    build: Literal['RELEASE', 'DEBUG']='RELEASE'
                    ) -> str:
    """Extracts the closest matching asset from a GitHub release url."""
    if '/releases/' not in url:
      raise ValueError(f'URL must resolve to a GitHub release.')

    # Get the release assets for a given release url
    release_catalog = github_release_catalog(url)
    assets = release_catalog['assets']
    if not len(assets):
      raise ValueError(f'Release catalog for {name} has no assets.')
    
    name_parts = split('-|_| ', name.lower())
    def get_match(arr: List[dict], cutoff=0.5):
      """Finds the closest kext bundle in a list of release assets."""
      closest = get_close_matches(name, [a['name'] for a in arr], n=1, cutoff=cutoff)
      if not closest or not any([ s in closest[0].lower() for s in name_parts ]):
        raise ValueError(f'Unable to resolve {name}.')
      return next(a['browser_download_url'] for a in arr if a['name'] == closest[0])

    # Get the asset with the closest name to the resolver and build target
    asset = None
    has_name = lambda asset: all([ s in asset['name'].lower() for s in name_parts ])
    has_build = lambda asset: build.lower() in asset['name'].lower()
    # Handle case where there is no clear resolution of the desired kext
    # i.e. there is no release asset with the same name and build
    if arr := list(filter(lambda a: not (has_name(a) and has_build(a)), assets)):
      asset = get_match(arr)
    # Handle case where there are no build targets
    elif arr := list(filter(lambda a: has_name(a) and not has_build(a), assets)):
      asset = get_match(arr)
    # Handle ambiguous or close matches
    elif arr := list(filter(lambda a: has_name(a) and has_build(a), assets)):
      asset = get_match(arr)

    return asset

  def resolve(self: TGitHubResolver,
              build: Literal['RELEASE', 'DEBUG']='RELEASE'
              ) -> str:
    """Returns a URL based on the class parameters."""
    params = dict(self)
    # Resolve version tag
    if self.has_any('tag'):
      tags = github_tag_names(repository=params['repository'])
      params['tag'] = resolve_version_specifier(versions=tags,
                                                specifier=params['tag'])
      # Handle non-standard semver tags
      if params['tag'] not in tags:
        tag_matches = get_close_matches(params['tag'], tags)
        if not tag_matches:
          raise ValueError(f"No matching tags found for {params['tag']}")
        params['tag'] = tag_matches[0]
    # Return raw file url
    if self.has_any('path'):
      return github_file_url(**params, raw=True)
    # Resolve artifact from latest workflow run
    if self.has_any('branch', 'workflow', 'commit'):
      return github_artifacts_url(**params)
    # Return the latest release (default) or by tag
    release_url = github_release_url(**params)
    if (name := self.__name__):
      # Return release asset url if name is provided
      return self.extract_asset(name, url=release_url, build=build)
    return release_url

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

  def glob(self: TPathResolver, pattern: str) -> Generator[TPathResolver, any, None]:
    """Iterates from a directory or from a file's parent directory."""
    glob_iter = None
    if self.resolve().is_file():
      glob_iter = self.resolve().parent.glob(pattern)
    else:
      glob_iter = self.resolve().glob(pattern)
    # Re-initialize PathResolver instances
    return (PathResolver(p) for p in glob_iter)

  def relative(self: TPathResolver, path: Union[str, TPathResolver]) -> str:
    """Resolves a relative representation from a path."""
    parent_dir = cls(path).resolve()
    if self.resolve().is_file():
      parent_dir = parent_dir.parent
    return self.relative_to(parent_dir).as_posix().__str__()
  
  def resolve(self: TPathResolver, strict: bool = False) -> cls:
    """Resolves a filepath based on the class parameters."""
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


__all__ = [
  # Classes (3)
  "GitHubResolver",
  "DortaniaResolver",
  "PathResolver"
]
