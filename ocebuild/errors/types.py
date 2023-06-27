## @file
# Validation methods used for testing and at runtime.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##


class GitHubRateLimit(Exception):
  """Indicates that the GitHub API rate limit has been exceeded."""
  def __init__(self,
               message: str,
               rate_limit: dict):
    super().__init__(message)
    #TODO: Include rate limit information.

class PathValidationError(Exception):
  """Indicates that a path does not match a given tree schema."""
  def __init__(self,
               message: str,
               name: str,
               path: str,
               kind: str):
    super().__init__(message)
    self.name = name
    self.path = path
    self.kind = kind
