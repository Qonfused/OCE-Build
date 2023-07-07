## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

from ocebuild import __file__
from ocebuild.sources.resolver import PathResolver


PROJECT_ROOT = PathResolver(__file__).parents[1]
"""The project's root directory."""

PROJECT_ENTRYPOINT = PathResolver(__file__).parent
"""The project's import entrypoint."""

MOCK_PATH = PROJECT_ROOT.joinpath('ci', 'mock')
"""The project's test mock directory."""


__all__ = [
  # Constants (3)
  "PROJECT_ROOT",
  "PROJECT_ENTRYPOINT",
  "MOCK_PATH"
]
