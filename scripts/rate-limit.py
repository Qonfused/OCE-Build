#!/usr/bin/env python3

## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Retrieve the GitHub API rate limit status."""

from rich.console import Console

from ocebuild.sources.github import github_rate_limit


if __name__ == '__main__':
  Console().print_json(data=github_rate_limit())
