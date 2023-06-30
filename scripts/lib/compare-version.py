#!/usr/bin/env python3

## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

from argparse import ArgumentParser
from platform import python_version

from packaging import version as pkgv


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument('--python-version',
                      default=python_version(),
                      help='python version to compare against (default: current python version)')
  parser.add_argument('--min',
                      help='minimum python version')
  parser.add_argument('--max',
                      help='maximum python version')
  args = parser.parse_args()

  # Get the current python version from virtenv
  version = args.python_version
  print(  f'python version: {version}')

  # Compare against min/max version (if provided)
  exit_code: int=0
  if (min_version := args.min):
    print(f'min_version:    {min_version}')
    exit_code = int(not pkgv.parse(min_version) <= pkgv.parse(version))
  if (max_version := args.max):
    print(f'max_version:    {max_version}')
    exit_code = int(not pkgv.parse(max_version) >= pkgv.parse(version))
  exit(exit_code)
