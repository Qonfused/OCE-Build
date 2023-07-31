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
  """Injects a module into the current Python runtime.

  This will override all consumers of the module, which may cause unexpected
  behavior if the new module is not compatible with the current runtime.

  Note that if a module is imported before this function is called, it will not
  be updated with the new module. This is useful for overriding modules that are
  imported by other dependencies or library consumers.

  Use this function with extreme caution!

  Args:
    name: The name of the module to inject.
    module: The module path to inject.
  """
  sys.modules[name] = import_module(module)

def inject_module_namespace(module,
                            exclude: Optional[set]=None,
                            namespace=globals()
                            ) -> Set[str]:
  """Injects all exported names from a module into the current namespace.

  This excludes built-ins and duplicate names to ensure no existing names are
  overwritten. This is useful for extending existing modules that may have
  internal names that are not exported.

  Args:
    module: The module to inject.
    exclude: A set of names to exclude from the module. (Optional)
    namespace: The namespace to inject the module into. (Default: globals())

  Returns:
    A set of all injected names.
  """
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
