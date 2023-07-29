#!/usr/bin/env python3

## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Compares a python version against a set of min/max constraints."""

import sys
from argparse import ArgumentParser
from platform import python_version as platform_version

from typing import Optional

from packaging import version as pkgv


def _main(python_version: Optional[str] = None,
          min_version: Optional[bool] = None,
          max_version: Optional[bool] = None,
          ) -> bool:
  # Get the current python version from virtenv
  version = python_version
  if not version: version = platform_version()
  print(  f'python version: {version}')

  # Compare against min/max version (if provided)
  result = True
  if min_version:
    print(f'min version:    {min_version}')
    result = pkgv.parse(min_version) <= pkgv.parse(version)
  if max_version:
    print(f'max version:    {max_version}')
    result = pkgv.parse(max_version) >= pkgv.parse(version)

  # Return result as boolean
  print(  f'result:         {result}')
  return result

if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument('--version', '--python-version',
                      nargs='?',
                      help='The python version to compare against.')
  parser.add_argument('--min', '--min-version',
                      help='The minimum python version allowed.')
  parser.add_argument('--max', '--max-version',
                      help='The maximum python version allowed.')
  args = parser.parse_args()

  res = _main(python_version=args.version,
              min_version=args.min,
              max_version=args.max)
  sys.exit(int(not res))


__all__ = []
