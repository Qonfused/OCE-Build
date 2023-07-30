#pragma no-implicit

## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Vendored third-party dependencies"""

import sys
from importlib import import_module

from typing import Optional, Set


def inject_module(name: str, module: str) -> None:
  """Injects a module into the current Python runtime."""
  sys.modules[name] = import_module(module)

def inject_module_namespace(module,
                            exclude: Optional[set]=None,
                            namespace=globals()
                            ) -> Set[str]:
  """Returns a list of all exported names from a module."""
  def get_export(name: str) -> any:
    return getattr(module, name)

  # Get all module names
  names = set(dir(module))
  # Remove all module built-ins and imports
  names -= set(module.__builtins__)
  names -= set(m for m in names if getattr(get_export(m), '__loader__', None))
  # Prune any excluded names
  if exclude: names -= set(exclude)
  # Prune any existing names from the current module
  names -= set(namespace)

  # Merge all module names into the current namespace's globals()
  for name in names:
    namespace[name] = get_export(name)

  return names


__all__ = [
  # Functions (2)
  'inject_module',
  "inject_module_namespace"
]
