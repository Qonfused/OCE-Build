## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Custom specifier resolver classes and methods."""

#pylint: disable=C0103,R1725,W0401,W0613,W0614,W0622,W1113,E0602

import re
from difflib import get_close_matches
from hashlib import sha256
from re import split

from typing import Generator, List, Literal, Optional, Tuple, TypeVar, Union

from .dortania import *
from .github import *

from ocebuild.versioning.semver import get_version, resolve_version_specifier

from third_party.cpython.pathlib import Path


TBaseResolver = TypeVar("TBaseResolver", bound="BaseResolver")
"""Internal type alias to BaseResolver
@internal
"""
TGitHubResolver = TypeVar("TGitHubResolver", bound="GitHubResolver")
"""Internal type alias to GitHubResolver
@internal
"""
TDortaniaResolver = TypeVar("TDortaniaResolver", bound="DortaniaResolver")
"""Internal type alias to DortaniaResolver
@internal
"""
TPathResolver = TypeVar("TPathResolver", bound="PathResolver")
"""Internal type alias to PathResolver
@internal
"""

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
               tarball: Optional[bool]=False,
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
    # Optional flags
    self.tarball = tarball

  @staticmethod
  def extract_asset(resolver: Union[TGitHubResolver, TDortaniaResolver],
                    name: str,
                    url: str,
                    build: Optional[Literal['RELEASE', 'DEBUG']]=None
                    ) -> str:
    """Extracts the closest matching asset from a GitHub release url."""
    if '/releases/' not in url:
      raise ValueError('URL must resolve to a GitHub release.')
    if build is None: build = 'RELEASE'
    resolver.build = build

    release_catalog = github_release_catalog(url)

    # Get the release assets for a given release url
    assets = release_catalog['assets']
    exclusion_list = {'debug-symbols'}
    assets = list(filter(lambda a: not any(s in a['name'].lower()
                                           for s in exclusion_list),
                         assets))
    if not assets:
      raise ValueError(f'Release catalog for {name} has no assets.')

    # Split tokens on capital letters, dashes, and underscores
    name_parts = split('-|_| ', re.sub( r"([A-Z])", r"-\1", name).lower())
    def get_match(arr: List[dict], cutoff=0.25, target=name):
      """Finds the closest kext bundle in a list of release assets."""
      closest = get_close_matches(target, [a['name'] for a in arr], 1, cutoff)
      if not closest or not any(s in closest[0].lower() for s in name_parts):
        # Fallback to the repo name if the kext name isn't listed in the assets
        repo_name = resolver.repository.rsplit('/', 1)[-1]
        if name != repo_name:
          return get_match(arr, target=repo_name)
        else:
          raise ValueError(f'Unable to resolve {target}.')
      return next(a['browser_download_url'] for a in arr if a['name'] == closest[0])

    # Get the asset with the closest name to the resolver and build target
    asset = None
    def with_name(asset):
      return all(s in asset['name'].lower() for s in name_parts)
    def with_build(asset):
      return build.lower() in asset['name'].lower()
    # Handle ambiguous or close matches
    if arr := list(filter(lambda a: with_name(a) and with_build(a), assets)):
      asset = get_match(arr)
    # Handle case where there are no build targets
    elif arr := list(filter(lambda a: with_name(a) and not with_build(a), assets)):
      asset = get_match(arr)
    # Handle case where there is no clear resolution of the desired kext
    # i.e. there is no release asset with the same name and build
    elif arr := list(filter(lambda a: not (with_name(a) and with_build(a)), assets)):
      asset = get_match(arr)

    # Store the asset version
    if release_catalog['tag_name'].count('.'):
      release_version = get_version(release_catalog['tag_name'])
    else:
      release_version = None

    # Do a best attempt of extracting the version from the asset name
    if not release_version:
      #TODO: Ensure case where the release tag is not a valid version is handled
      try:
        asset_metastring = "-".join(asset.split('/')[-1].split('-')[1:]) \
          .lower() \
          .replace(f'-{build.lower()}', '')
        version_parts = asset_metastring.split('.')[:-1]
        release_version = get_version(".".join(version_parts))
      except Exception: pass

    # Extract only the public semver properties for the resolver
    if release_version:
      resolver.version = ".".join(map(str, release_version.release))

    return asset

  def resolve(self: TGitHubResolver,
              build: Optional[Literal['RELEASE', 'DEBUG']]=None
              ) -> str:
    """Returns a URL based on the class parameters."""
    params = dict(self)
    repo = params['repository']

    # Handle case where a commit is not normally resolved
    def _clamp_commit():
      """Clamp down ambiguous commit resolution"""
      if not self.has_any('commit'):
        # Resolve the latest commit for the given branch
        _args = { k:v for k,v in params.items() if k in ('repository', 'branch') }
        _commit = get_latest_commit(**_args)
        self.commit = _commit
        params['commit'] = _commit

    # Return archive url
    if params.get('tarball'):
      _clamp_commit()
      _args = { k:v for k,v in params.items() if k not in ('tarball') }
      return github_archive_url(**_args)
    else:
      del params['tarball']

    # Return raw file url
    if self.has_any('path'):
      _clamp_commit()
      return github_file_url(**params, raw=True)

    # Resolve version tag
    if self.has_any('tag'):
      input_tag = params['tag']
      tags, commits = github_tag_names(repository=params['repository'],
                                       get_commits=True)
      params['tag'] = resolve_version_specifier(versions=tags,
                                                specifier=input_tag)
      if params['tag'] is None:
        raise ValueError(f"{repo} - Could not resolve a tag for '{input_tag}'")
      # Handle non-standard semver tags
      if params['tag'] not in tags:
        tag = params['tag']
        tag_matches = get_close_matches(tag, tags)
        if not tag_matches:
          raise ValueError(f"{repo} - No matching tags found for '{tag}'")
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
  def has_build(plugin: str):
    return has_build(plugin=plugin)

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

class PathResolver(BaseResolver, Path):
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

  def glob(self: TPathResolver,
           pattern: str
           ) -> Generator[TPathResolver, any, None]:
    """Iterates from a directory or from a file's parent directory."""
    cls = self.resolve().__getinstance__()

    glob_iter = None
    if cls.is_file():
      glob_iter = cls.parent.glob(pattern)
    else:
      glob_iter = cls.glob(pattern)
    # Re-initialize PathResolver instances
    return (PathResolver(p) for p in glob_iter)

  def resolve(self: TPathResolver, strict: bool = False) -> Path:
    """Resolves a filepath based on the class parameters.

    If the path exists, the checksum is calculated and stored.

    Args:
      strict: If True, raises an error if the path does not exist.

    Returns:
      The resolved filepath wrapped in a PathResolver instance.
    """

    cls = self.__getinstance__().__class__
    resolved_path = cls(self.path).resolve(strict=strict)

    if strict or resolved_path.exists():
      # Get checksum of the resolved filepath
      from .binary import get_digest #pylint: disable=import-outside-toplevel
      self.checksum = get_digest(resolved_path, algorithm=sha256)

    #TODO: Handle additional path type verifications here
    return resolved_path

ResolverType = Union[GitHubResolver, DortaniaResolver, PathResolver]
"""A type alias for the Resolver classes."""


__all__ = [
  # Variables (1)
  "ResolverType",
  # Classes (3)
  "GitHubResolver",
  "DortaniaResolver",
  "PathResolver"
]
