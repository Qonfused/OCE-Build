#!/usr/bin/env python3

## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Stub entry point for the CLI."""

from ocebuild_cli.__main__ import _main as _cli

def _main():
  _cli()

if __name__ == '__main__':
  _main()
