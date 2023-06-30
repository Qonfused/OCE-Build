## @file
# Methods for formatting and retrieving GitHub source URLs.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

from datetime import datetime, timedelta
from functools import partial
from urllib.request import Request

from typing import List, Optional, Union

from ocebuild.errors._lib import disable_exception_traceback
from ocebuild.errors.types import GitHubRateLimit
from ocebuild.parsers.dict import nested_get
from ocebuild.sources._lib import request
from ocebuild.constants import ENV


def github_api_request(endpoint: Optional[str]=None,
                       url: Optional[str]=None
                       ) -> any:
  """Gets a GitHub API request.

  Args:
    endpoint: GitHub API endpoint.

  Returns:
    API response.
  """
  req = Request(f'https://api.github.com{endpoint}' if not url else url)
  if ENV.has('GITHUB_TOKEN'):
    req.add_header('Authorization', f'token {ENV.GITHUB_TOKEN}')
  return request(req)

################################################################################
#                               API Request Guards                             #
################################################################################

def github_rate_limit(kind: str='core', raise_error: float=False) -> int:
  """Gets the GitHub API rate limit.

  Args:
    kind: The kind of GitHub API request to query.
    raise_error: Raise an exception if the rate limit has been exceeded.

  Returns:
    Remaining API calls allowed.
  
  Raises:
    Exception: If the rate limit has been exceeded.
  """
  rate_limit = github_api_request('/rate_limit').json()
  if not raise_error:
    if kind: return nested_get(rate_limit, ['resources', kind])
    return rate_limit
  elif nested_get(rate_limit, ['resources', kind, 'remaining']) == 0:
    current_time = datetime.now()
    reset_time = datetime.fromtimestamp(
        nested_get(rate_limit, ['resources', kind, 'reset']))
    # Format remaining time in a friendly way for error message
    msg = partial('{} requests exceeded. Try again in {} {}.'.format,
                  kind.capitalize())
    if (mins := round((reset_time - current_time) / timedelta(minutes=1))):
      msg = msg(mins, 'minutes' if mins != 1 else 'minute')
    elif (secs := round((reset_time - current_time) / timedelta(seconds=1))):
      msg = msg(secs, 'seconds' if secs != 1 else 'second')
    # Raise error without stacktrace
    with disable_exception_traceback():
      raise GitHubRateLimit(msg, rate_limit)

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
  try:
    suites_endpoint = f'/repos/{repository}/commits/{commit}/check-suites'
    for suite in github_api_request(suites_endpoint).json()['check_suites']:
      check_runs_url = suite['check_runs_url']
      if status and suite['status'] != status: continue
      # Enumerate suites for matching workflow ids
      for run in github_api_request(url=check_runs_url).json()['check_runs']:
        if f'/runs/{workflow_id}/jobs/' in run['details_url']:
          return nested_get(run, ['check_suite', 'id'])
    # No matching suite found
    return None
  except:
    if not github_rate_limit(raise_error=True): raise

def github_tag_names(repository: str) -> List[str]:
  """Returns a list of all repository tags.

  Args:
    repository: GitHub repository name.

  Returns:
    List of repository tags.
  """
  try:
    tags_endpoint = f"/repos/{repository}/tags"
    return [tag['name'] for tag in github_api_request(tags_endpoint).json()]
  except:
    if not github_rate_limit(raise_error=True): raise

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
  
  if not tag:
    try:
      tags_catalog = github_api_request(f'/repos/{repository}/tags').json()
      tag = tags_catalog[0]['name']
    except:
      if not github_rate_limit(raise_error=True): raise
  return f'https://github.com/{repository}/releases/tag/{tag}'

def github_artifacts_url(repository: str,
                         branch: Optional[str]=None,
                         workflow: Optional[str]=None,
                         commit: Optional[str]=None
                         ) -> Union[str, None]:
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
      workflows_endpoint = f'/repos/{repository}/actions/workflows'
      for w in github_api_request(workflows_endpoint).json():
        if workflow == w['name']: workflow_id = w['id']; break
    # Filter artifact urls
    artifacts_endpoint = f'/repos/{repository}/actions/artifacts'
    catalog = github_api_request(artifacts_endpoint).json()
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
      if (suite_id := github_suite_id(repository, head_sha, w_id)):
        return f'https://github.com/{repository}/suites/{suite_id}/artifacts/{id}'
  except:
    if not github_rate_limit(raise_error=True): raise
  return None