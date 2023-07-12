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

from .dortania import *
from .github import *

from ocebuild.versioning.semver import get_version, resolve_version_specifier


TBaseResolver = TypeVar("TBaseResolver", bound="BaseResolver")
TGitHubResolver = TypeVar("TGitHubResolver", bound="GitHubResolver")
TDortaniaResolver = TypeVar("TDortaniaResolver", bound="DortaniaResolver")
TPathResolver = TypeVar("TPathResolver", bound="PathResolver")

class BaseResolver():
  """Base resolver class implementing overrides.

  This class is used to store custom specifier methods and metadata.
  @internal
  """

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
  def extract_asset(self: Union[TGitHubResolver, TDortaniaResolver],
                    name: str,
                    url: str,
                    build: Optional[Literal['RELEASE', 'DEBUG']]=None
                    ) -> str:
    """Extracts the closest matching asset from a GitHub release url."""
    if '/releases/' not in url:
      raise ValueError(f'URL must resolve to a GitHub release.')
    if build is None: build = 'RELEASE'
    self.build = build

    release_catalog = github_release_catalog(url)

    # Get the release assets for a given release url
    assets = release_catalog['assets']
    if not len(assets):
      raise ValueError(f'Release catalog for {name} has no assets.')
    
    name_parts = split('-|_| ', name.lower())
    def get_match(arr: List[dict], cutoff=0.25):
      """Finds the closest kext bundle in a list of release assets."""
      closest = get_close_matches(name, [a['name'] for a in arr], n=1, cutoff=cutoff)
      if not closest or not any([ s in closest[0].lower() for s in name_parts ]):
        raise ValueError(f'Unable to resolve {name}.')
      return next(a['browser_download_url'] for a in arr if a['name'] == closest[0])

    # Get the asset with the closest name to the resolver and build target
    asset = None
    has_name = lambda asset: all([ s in asset['name'].lower() for s in name_parts ])
    has_build = lambda asset: build.lower() in asset['name'].lower()
    # Handle ambiguous or close matches
    if arr := list(filter(lambda a: has_name(a) and has_build(a), assets)):
      asset = get_match(arr)
    # Handle case where there are no build targets
    elif arr := list(filter(lambda a: has_name(a) and not has_build(a), assets)):
      asset = get_match(arr)
    # Handle case where there is no clear resolution of the desired kext
    # i.e. there is no release asset with the same name and build
    elif arr := list(filter(lambda a: not (has_name(a) and has_build(a)), assets)):
      asset = get_match(arr)
    
    # Store the asset version
    release_version = get_version(release_catalog['tag_name'])
    if not release_version:
      #TODO: Ensure case where the release tag is not a valid version is handled
      try:
        # Do a best attempt of extracting the version from the asset name
        asset_metastring = "-".join(asset.split('/')[-1].split('-')[1:]) \
          .lower() \
          .replace(f'-{build.lower()}', '')
        version_parts = asset_metastring.split('.')[:-1]
        release_version = get_version(".".join(version_parts))
      except: pass
    if release_version:
      self.version = ".".join(map(str, release_version.release))

    return asset

  def resolve(self: TGitHubResolver,
              build: Optional[Literal['RELEASE', 'DEBUG']]=None
              ) -> str:
    """Returns a URL based on the class parameters."""
    params = dict(self)
  
    # Return raw file url
    if self.has_any('path'):
      return github_file_url(**params, raw=True)

    # Resolve version tag
    if self.has_any('tag'):
      input_tag = params['tag']
      tags, commits = github_tag_names(repository=params['repository'],
                                       get_commits=True)
      params['tag'] = resolve_version_specifier(versions=tags,
                                                specifier=input_tag)
      if params['tag'] is None:
        raise ValueError(f"{params['repository']} - Could not resolve a tag for '{input_tag}'")
      # Handle non-standard semver tags
      if params['tag'] not in tags:
        tag_matches = get_close_matches(params['tag'], tags)
        if not tag_matches:
          raise ValueError(f"{params['repository']} - No matching tags found for '{params['tag']}'")
        params['tag'] = tag_matches[0]
      # Get the commit hash for the resolved tag
      self.commit = next((c for t,c in zip(tags, commits) if t == params['tag']),
                         self.commit)
    # Resolve artifact from latest workflow run
    elif self.has_any('branch', 'workflow', 'commit'):
      url, commit = github_artifacts_url(**params, get_commit=True)
      if not self.has_any('commit'):
        self.commit = commit
      return url
  
    # Return the latest release (default) or by tag
    release_url = github_release_url(**params)
    if (name := self.__name__):
      # Return release asset url if name is provided
      return self.extract_asset(self, name, url=release_url, build=build)
  
    return release_url

class DortaniaResolver(BaseResolver):
  """Resolves a Dortania build URL based on the class parameters."""

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
  
  @staticmethod
  def has_build(plugin: str): return has_build(plugin=plugin)

  def resolve(self: TDortaniaResolver,
              build: Optional[Literal['RELEASE', 'DEBUG']]=None
              ) -> str:
    """Returns a URL based on the class parameters."""
    if not build: build = self.build
    plugin = self.__name__
    params = dict(self)
  
    # Resolve build commit sha
    commit_sha: str
    if self.has_any('commit'):
      commit_sha = params['commit']
    else:
      commit_sha = get_latest_sha(plugin)
      self.commit = commit_sha
    
    # Return the latest build (default) or by commit sha
    release_url = dortania_release_url(plugin, commit=commit_sha)
    if build is not None:
      # Return release asset url if name is provided
      return GitHubResolver.extract_asset(self,
                                          name=plugin,
                                          url=release_url,
                                          build=build)
  
    return release_url

class PathResolver(BaseResolver, cls := type(Path())):
  """Resolves a filepath based on the class parameters."""

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

  def relative(self: TPathResolver,
               path: Union[str, TPathResolver]='.',
               from_parent: bool=False
               ) -> str:
    """Resolves a relative representation from a path."""
    parent_dir = cls(path).resolve()
    if from_parent and self.resolve().is_file():
      parent_dir = parent_dir.parent
    return self.relative_to(parent_dir).as_posix()
  
  def resolve(self: TPathResolver,
              strict: bool = False
              ) -> cls:
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

ResolverType = Union[GitHubResolver, DortaniaResolver, PathResolver]


__all__ = [
  "ResolverType",
  # Variables (4)
  "TBaseResolver",
  "TGitHubResolver",
  "TDortaniaResolver",
  "TPathResolver",
  # Classes (3)
  "GitHubResolver",
  "DortaniaResolver",
  "PathResolver"
]
