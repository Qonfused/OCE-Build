## @file
# Methods for formatting and retrieving source URLs.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

from json import load as json_load
from ssl import _create_unverified_context as skip_ssl_verify
from urllib.request import urlopen, Request

from typing import List, Optional, Union

from parsers.dict import nested_get


def request(url: Union[str, Request]) -> any:
  """Simple wrapper over urlopen for skipping SSL verification."""
  return urlopen(url, context=skip_ssl_verify())

################################################################################
#                     Parameter formatting/retrival functions                  #
################################################################################

def github_suite_id(repository: str,
                    commit: str,
                    workflow_id: int,
                    status: Optional[str]='completed'
                    ) -> Union[int, None]:
  """Gets the GitHub check suite ID for a given commit.

  Args:
    repository: GitHub repository name.
    commit: Commit hash.

  Returns:
    Check suite ID.
  """
  suites_url = f'https://api.github.com/repos/{repository}/commits/{commit}/check-suites'
  for suite in json_load(request(suites_url))['check_suites']:
    check_runs_url = suite['check_runs_url']
    if status and suite['status'] != status: continue
    # Enumerate suites for matching workflow ids
    for run in json_load(request(check_runs_url))['check_runs']:
      if f'/runs/{workflow_id}/jobs/' in run['details_url']:
        return nested_get(run, ['check_suite', 'id'])
  return None

################################################################################
#                        URL formatting/retrieval functions                    #
################################################################################

def github_file_url(repository: str,
                    path: str,
                    branch: str='main',
                    tag: Optional[str]=None,
                    commit: Optional[str]=None,
                    raw: bool=False
                    ) -> str:
  """Formats a GitHub file URL.

  Args:
    repository: GitHub repository name.
    path: Relative path to file.
    branch: Branch name.
    tag: Tag name.
    commit: Commit hash.
    raw: If True, returns the raw URL.

  Returns:
    URL of the file.
  
  Example:
    >>> github_file_url('foo/bar', path='file.json')
    # -> "https://github.com/foo/bar/blob/main/file.json"
    >>> github_file_url('foo/bar', path='file.json', branch='dev')
    # -> "https://github.com/foo/bar/blob/dev/file.json"
    >>> github_file_url('foo/bar', path='file.json', tag='v1.0.0')
    # -> "https://github.com/foo/bar/blob/v1.0.0/file.json"
    >>> github_file_url('foo/bar', path='file.json', commit='c0ffee')
    # -> "https://github.com/foo/bar/blob/c0ffee/file.json"
    >>> github_file_url('foo/bar', path='file.json', raw=True)
    # -> "https://raw.githubusercontent.com/foo/bar/main/file.json"
  """
  prefix = 'github.com' if not raw else 'raw.githubusercontent.com'
  stem = 'blob/' if not raw else ''
  if commit:
    return f'https://{prefix}/{repository}/{stem}{commit}/{path}'
  if tag:
    return f'https://{prefix}/{repository}/{stem}{tag}/{path}'
  return f'https://{prefix}/{repository}/{stem}{branch}/{path}'

def github_archive_url(repository: str,
                       branch: str='main',
                       tag: Optional[str]=None,
                       commit: Optional[str]=None
                       ) -> str:
  """Formats a GitHub archive URL.

  Args:
    repository: GitHub repository name.
    branch: Branch name.
    tag: Tag name.
    commit: Commit hash.

  Returns:
    URL of the archive.
  
  Example:
    >>> github_archive_url('foo/bar')
    # -> "https://github.com/foo/bar/archive/refs/heads/main.tar.gz"
    >>> github_archive_url('foo/bar', branch='dev')
    # -> "https://github.com/foo/bar/archive/refs/heads/dev.tar.gz"
    >>> github_archive_url('foo/bar', tag='v1.0.0')
    # -> "https://github.com/foo/bar/archive/refs/tags/v1.0.0.tar.gz"
    >>> github_archive_url('foo/bar', commit='c0ffee')
    # -> "https://github.com/foo/bar/archive/c0ffee.tar.gz"
  """
  if commit:
    return f'https://github.com/{repository}/archive/{commit}.tar.gz'
  if tag:
    return f'https://github.com/{repository}/archive/refs/tags/{tag}.tar.gz'
  return f'https://github.com/{repository}/archive/refs/heads/{branch}.tar.gz'

def github_release_url(repository: str,
                       tag: Optional[str]=None
                       ) -> str:
  """Formats a GitHub release URL.

  Args:
    repository: GitHub repository name.
    tag: Tag name.

  Returns:
    URL of the release.
  
  Example:
    >>> github_release_url('foo/bar')
    # -> "https://github.com/foo/bar/releases/latest/v2.0.0"
    >>> github_release_url('foo/bar', tag='v1.0.0')
    # -> "https://github.com/foo/bar/releases/tag/v1.0.0"
  """
  try:
    if not tag:
      catalog_url = f'https://api.github.com/repos/{repository}/tags'
      with json_load(request(catalog_url)) as tags_catalog:
        tag = tags_catalog[0]['name']
  finally:
    return f'https://github.com/{repository}/releases/tag/{tag}'

def github_artifacts_url(repository: str,
                         branch: Optional[str]=None,
                         workflow: Optional[str]=None,
                         commit: Optional[str]=None
                         ) -> Union[List[str], None]:
  """Formats a GitHub artifacts URL.

  Args:
    repository: GitHub repository name.
    branch: Branch name.
    tag: Tag name.
    commit: Commit hash.

  Returns:
    URL of the artifacts archive.
  """
  try:
    # Get workflow id (if workflow name is provided)
    workflow_id: int=None
    if workflow is not None:
      workflows_url = f'https://api.github.com/repos/{repository}/actions/workflows'
      for w in json_load(request(workflows_url)):
        if workflow == w['name']: workflow_id = w['id']; break
    # Filter artifact urls
    catalog_url = f'https://api.github.com/repos/{repository}/actions/artifacts'
    catalog = json_load(request(catalog_url))
    for workflow_run in catalog['artifacts']:
      id = workflow_run['id']
      w_id = nested_get(workflow_run, ['workflow_run', 'id'])
      head_branch = nested_get(workflow_run, ['workflow_run', 'head_branch'])
      head_sha = nested_get(workflow_run, ['workflow_run', 'head_sha'])
      # Filter run by given parameters
      if branch and branch != head_branch: continue
      if workflow_id and workflow_id != w_id: continue
      if commit and commit != head_sha: continue
      # Return the first matching artifact url
      if (suite_id := github_suite_id(repository, commit, w_id)):
        return f'https://github.com/{repository}/suites/{suite_id}/artifacts/{id}'
  except: pass
  return None
