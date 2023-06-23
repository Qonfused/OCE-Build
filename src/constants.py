## @file
#
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##


def github_file_url(repository: str,
                    path: str,
                    branch: str='main',
                    tag: str=None,
                    commit: str=None,
                    raw: bool=False) -> str:
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
  if branch:
    return f'https://{prefix}/{repository}/{stem}{branch}/{path}'

def github_archive_url(repository: str,
                       branch: str='main',
                       tag: str=None,
                       commit: str=None) -> str:
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
  if branch:
    return f'https://github.com/{repository}/archive/refs/heads/{branch}.tar.gz'


DORTANIA_BUILD_CATALOG = github_file_url('dortania/build-repo', 'config.json', branch='builds')

OC_PKG_URL = github_archive_url('acidanthera/OpenCorePkg', branch='master')
OC_BIN_URL = github_archive_url('acidanthera/OcBinaryData', branch='master')
