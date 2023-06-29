## @file
# Methods for formatting and retrieving Dortania source URLs.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

from datetime import datetime, timezone

from typing import Optional

from parsers.dict import nested_get
from sources._lib import request
from sources.github import github_file_url, github_release_url


DORTANIA_LAST_UPDATED: datetime
DORTANIA_LATEST_BUILDS: dict
DORTANIA_LISTED_BUILDS: dict

################################################################################
#                               API Request Guards                             #
################################################################################

def is_latest_build() -> bool:
  """Checks if the build catalog is latest."""
  timestamp = datetime.now(tz=timezone.utc)
  # Only re-validate 30 minutes after the last update
  if (timestamp - DORTANIA_LAST_UPDATED) <= datetime.timedelta(minutes=30):
    return True
  # Revalidate build catalog timestamp
  latest_timestamp = datetime.fromisoformat(
      request(dortania_file_url('last_updated.txt')).text().read())
  if latest_timestamp > DORTANIA_LAST_UPDATED:
    DORTANIA_LAST_UPDATED = latest_timestamp
    return False
  return True

def has_build(plugin: str) -> str:
  """Checks if a plugin has a build."""
  # Revalidates build catalog cache
  if not is_latest_build():
    DORTANIA_LISTED_BUILDS = request(dortania_file_url('plugins.json')).json()
  # Check if plugin is in the build catalog
  return plugin in DORTANIA_LISTED_BUILDS

################################################################################
#                     Parameter formatting/retrival functions                  #
################################################################################

def get_latest_sha(plugin: str) -> str:
  """Gets the latest build sha for a plugin."""
  if not has_build(plugin):
    raise ValueError(f'Plugin {plugin} not in Dortania build catalog.')
  # Revalidates build catalog cache
  if not is_latest_build():
    DORTANIA_LATEST_BUILDS = request(dortania_file_url('latest.json')).json()
  # Returns the latest build sha
  try:
    return nested_get(DORTANIA_LATEST_BUILDS,
                      keys=[plugin, 'versions', 0, 'commit', 'sha'])
  except:
    raise ValueError(f'Plugin {plugin} has no builds listed.')

################################################################################
#                        URL formatting/retrieval functions                    #
################################################################################

def dortania_file_url(file: str):
  """Formats a Dortania build repo file URL."""
  return github_file_url(repository='dortania/build-repo',
                         branch='builds',
                         path=file,
                         raw=True)

def dortania_release_url(plugin: str,
                         commit: Optional[str]=None) -> str:
  """Formats a Dortania build release URL."""
  if not has_build(plugin):
    raise ValueError(f'Plugin {plugin} not in Dortania build catalog.')
  # Returns the latest build release (default) or by commit
  if not commit: commit = get_latest_sha(plugin)
  return github_release_url(repository='dortania/build-repo',
                            tag=f'{plugin}{commit[:7]}')
