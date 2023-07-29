#pragma no-implicit

## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Vendored third-party dependencies"""

import sys
from importlib import import_module


def inject_module(name: str, module: str) -> None:
  """Injects a module into the current Python runtime."""
  sys.modules[name] = import_module(module)


__all__ = [
  # Functions (1)
  'inject_module',
]
