## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

from os import environ as os_environ

from typing import Union


class EnvironWrapper:
  """Simple class to securely read environment variables."""
  def __init__(self):
    self.__signature__ = 'SECURE'

  def has(self, token: str) -> bool:
    """Checks if the given environment variable is set."""
    return getattr(self, token, None) is not None

  @property
  def GITHUB_TOKEN(self) -> Union[str, None]:
    """(Optional) A GitHub personal access token to authenticate API requests.

    It's recommended to use a fine-grained personal access token with access
    to public repositories (read-only) to grant required base permissions.
    @see https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens

    The token can be created in the GitHub settings page.
    @see https://github.com/settings/tokens?type=beta
    """
    return os_environ.get('GITHUB_TOKEN')

ENV = EnvironWrapper()
