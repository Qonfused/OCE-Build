## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

from ocebuild.sources.resolver import PathResolver
from ocebuild import __file__


PROJECT_ROOT = PathResolver(__file__).parents[1]
"""The project's root directory."""

PROJECT_ENTRYPOINT = PathResolver(__file__).parent
"""The project's import entrypoint."""


__all__ = [
  # Constants (2)
  "PROJECT_ROOT",
  "PROJECT_ENTRYPOINT"
]
