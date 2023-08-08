#!/usr/bin/env python3

## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Retrieve the GitHub API rate limit status."""

from datetime import datetime, timedelta
from functools import partial

from rich.console import Console

#pragma preserve-imports - Inject project namespaces into the module search path
import sys, pathlib; sys.path.insert(1, str(pathlib.Path(__file__, '../' * 4).resolve()))

from ocebuild.sources.github import github_rate_limit


if __name__ == '__main__':
  rate_limit = github_rate_limit()

  # Format reset time in a human readable format.
  msg = partial('Resets in {} {}.'.format)
  current_time = datetime.now()
  reset_time = datetime.fromtimestamp(rate_limit['reset'])
  if (mins := round((reset_time - current_time) / timedelta(minutes=1))):
    msg = msg(mins, 'minutes' if mins != 1 else 'minute')
  elif (secs := round((reset_time - current_time) / timedelta(seconds=1))):
    msg = msg(secs, 'seconds' if secs != 1 else 'second')

  console = Console()
  console.print(msg)
  console.print_json(data=github_rate_limit())
