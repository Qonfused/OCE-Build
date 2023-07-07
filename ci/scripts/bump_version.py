#!/usr/bin/env python3

## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Bumps the project version using the given semver string."""

from argparse import ArgumentParser

from types import SimpleNamespace
from typing import Optional

from ci import PROJECT_ROOT

from ocebuild.parsers.regex import re_search
from ocebuild.sources.resolver import PathResolver
from ocebuild.version import __file__ as __version_file__, __version__
from ocebuild.version import _BUILD, _MAJOR_VERSION, _MINOR_VERSION, _PATCH_VERSION, _PRE_RELEASE


version = SimpleNamespace(major=int(_MAJOR_VERSION),
                          minor=int(_MINOR_VERSION),
                          patch=int(_PATCH_VERSION),
                          pre_release=_PRE_RELEASE,
                          build=int(_BUILD))
"""Represents the current version of the project."""
    
def bump_version(major: Optional[bool]=None,
                 minor: Optional[bool]=None,
                 patch: Optional[bool]=None,
                 pre_release: Optional[str]=None,
                 build: Optional[bool]=None
                 ) -> str:
  """Bumps the project current version."""

  global version

  # Handle semver components
  if   major:
    version.major += 1; version.minor = 0; version.patch = 0
  elif minor:
    version.minor += 1; version.patch = 0
  elif patch:
    version.patch += 1
  # Handle increment of pre-release versions
  if   pre_release:
    version.pre_release = pre_release
    if '.' in _PRE_RELEASE and _PRE_RELEASE.split(".")[0] == pre_release:
      version.pre_release += f'.{int(_PRE_RELEASE.split(".")[-1]) + 1}'
    elif pre_release not in ('dev', 'release'):
      version.pre_release += '.1'
  # Handle increment and reset of build versions
  if build:
    version.build += 1
  else:
    version.build = 0

  return format_version(version)

def format_version(version: SimpleNamespace) -> str:
  """Formats the current version's semver components."""
  base_semver = f'{version.major}.{version.minor}.{version.patch}'
  if version.pre_release:
    base_semver += f'-{version.pre_release}'
  if version.build:
    base_semver += f'+{version.build}'
  return base_semver


def _main(**kwargs) -> None:
  # Bump the project version
  version_str = bump_version(**kwargs)

  # Update version file
  version_file = PathResolver(__version_file__)
  with open(version_file, 'r', encoding='UTF-8') as file:
    file_text = file.read()
    # Replace semver components
    file_text = file_text \
      .replace(f"_MAJOR_VERSION = {_MAJOR_VERSION}",
               f"_MAJOR_VERSION = {version.major}") \
      .replace(f"_MINOR_VERSION = {_MINOR_VERSION}",
               f"_MINOR_VERSION = {version.minor}") \
      .replace(f"_PATCH_VERSION = {_PATCH_VERSION}",
               f"_PATCH_VERSION = {version.patch}") \
      .replace(f"_PRE_RELEASE   = '{_PRE_RELEASE}'",
               f"_PRE_RELEASE   = '{version.pre_release}'") \
      .replace(f"_BUILD         = {_BUILD}",
               f"_BUILD         = {version.build}")
    # Replace semver string
    file_text = file_text \
      .replace(f"__version__    = '{__version__}'",
               f"__version__    = '{version_str}'")
    # Write to file
    PathResolver(version_file).write_text(file_text, encoding='UTF-8')
  
  # Update project config file
  project_cfg = PathResolver(PROJECT_ROOT, 'pyproject.toml')
  with open(project_cfg, 'r', encoding='UTF-8') as file:
    file_text = file.read()
    # Get version string pattern
    prefix = re_search(f'(version\\s*=\\s)"{__version__}"', file_text, 1)
    # Replace semver string
    file_text = file_text \
      .replace(f'{prefix}"{__version__}"',
               f'{prefix}"{version_str}"')
    # Write to file
    PathResolver(project_cfg).write_text(file_text, encoding='UTF-8')

  print(f"Bumped version from '{__version__}' to '{version_str}'")

if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument('--major',
                      action='store_true',
                      help='Bumps the version major.')
  parser.add_argument('--minor',
                      action='store_true',
                      help='Bumps the version minor.')
  parser.add_argument('--patch',
                      action='store_true',
                      help='Bumps the version patch.')
  parser.add_argument('--pre-release',
                      help='Sets the version pre-release.')
  parser.add_argument('--build',
                      action='store_true',
                      help='Bumps the version build.')
  args = parser.parse_args()

  _main(major=args.major,
        minor=args.minor,
        patch=args.patch,
        pre_release=args.pre_release,
        build=args.build)


__all__ = [
  # Variables (1)
  "version",
  # Functions (2)
  "bump_version",
  "format_version"
]
