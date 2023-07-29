## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Methods for formatting and retrieving Dortania source URLs."""

from datetime import datetime, timedelta, timezone

from typing import Optional

from ._lib import request
from .github import github_file_url, github_release_url

from ocebuild.parsers.dict import nested_get


DORTANIA_LAST_UPDATED: datetime=None
"""The last time the Dortania build catalog was updated."""

DORTANIA_LATEST_BUILDS: dict={}
"""The latest Dortania build catalog."""

DORTANIA_LISTED_BUILDS: set={}
"""Available plugins in the Dortania build catalog."""

################################################################################
#                               API Request Guards                             #
################################################################################

def is_latest_build() -> bool:
  """Checks if the cached build catalog is latest."""
  global DORTANIA_LAST_UPDATED

  timestamp = datetime.now(tz=timezone.utc)
  if not DORTANIA_LAST_UPDATED:
    pass #de-op
  # Only re-validate 30 minutes after the last update
  elif (timestamp - DORTANIA_LAST_UPDATED) <= timedelta(minutes=30):
    return True

  # Revalidate build catalog timestamp
  latest_timestamp = datetime.fromisoformat(
      request(dortania_file_url('last_updated.txt')).text().read())
  if not DORTANIA_LAST_UPDATED or latest_timestamp > DORTANIA_LAST_UPDATED:
    DORTANIA_LAST_UPDATED = latest_timestamp
    return False

  return True

def has_build(plugin: str) -> bool:
  """Checks if a plugin has a build."""
  global DORTANIA_LISTED_BUILDS
  # Revalidates build catalog cache
  if not is_latest_build():
    # print('Revalidating build catalog cache...')
    catalog = request(dortania_file_url('plugins.json')).json()
    DORTANIA_LISTED_BUILDS = set(catalog['plugins'])
  # Check if plugin is in the build catalog
  return plugin in DORTANIA_LISTED_BUILDS

################################################################################
#                     Parameter formatting/retrival functions                  #
################################################################################

def get_latest_sha(plugin: str) -> str:
  """Gets the latest build sha for a plugin."""
  global DORTANIA_LATEST_BUILDS
  if not has_build(plugin):
    raise ValueError(f'Plugin {plugin} not in Dortania build catalog.')
  # Revalidates build catalog cache
  if not DORTANIA_LATEST_BUILDS or not is_latest_build():
    DORTANIA_LATEST_BUILDS = request(dortania_file_url('latest.json')).json()
  # Returns the latest build sha
  return nested_get(DORTANIA_LATEST_BUILDS,
                    keys=[plugin, 'versions', 0, 'commit', 'sha'])

################################################################################
#                        URL formatting/retrieval functions                    #
################################################################################

def dortania_file_url(filepath: str) -> str:
  """Formats a Dortania build repo file URL.

  Args:
    file: The remote filepath of the file.

  Returns:
    The formatted Dortania build repo file URL.
  """
  return github_file_url(repository='dortania/build-repo',
                         branch='builds',
                         path=filepath,
                         raw=True)

def dortania_release_url(plugin: str,
                         commit: Optional[str]=None) -> str:
  """Formats a Dortania build release URL.

  Args:
    plugin: The plugin to get the release URL for.
    commit: The commit to get the release URL for. Defaults to the latest build.

  Returns:
    The formatted Dortania build release URL.
  """
  if not has_build(plugin):
    raise ValueError(f'Plugin {plugin} not in Dortania build catalog.')
  # Returns the latest build release (default) or by commit
  if not commit: commit = get_latest_sha(plugin)
  return github_release_url(repository='dortania/build-repo',
                            tag=f'{plugin}-{commit[:7]}')


__all__ = [
  # Functions (5)
  "is_latest_build",
  "has_build",
  "get_latest_sha",
  "dortania_file_url",
  "dortania_release_url"
]
