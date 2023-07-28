## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Constants used by the CI system."""

from sys import builtin_module_names
from sysconfig import get_paths

from ocebuild import __file__
from ocebuild.sources.resolver import PathResolver


def _enumerate_modules(path: str) -> set:
  """Returns a set of all modules in a directory."""
  files = set()
  for f in sorted(PathResolver(path).iterdir()):
    name = f.stem
    if f.is_dir() and f.joinpath('__init__.py').exists():
      files.add(name)
    elif f.is_file() and f.suffix == '.py':
      files.add(name)

  return files

################################################################################
#                              Project Constants                               #
################################################################################

PROJECT_ENTRYPOINT = PathResolver(__file__).parent
"""The main project's import entrypoint."""

PROJECT_ROOT = PathResolver(__file__).parents[1]
"""The project's root directory."""

PROJECT_DOCS = PROJECT_ROOT.joinpath('docs')
"""The project's documentation directory."""

PROJECT_EXAMPLES = PROJECT_ROOT.joinpath('examples')
"""The project's examples directory."""

PROJECT_NAMESPACES = _enumerate_modules(PROJECT_ROOT)
"""The project's root namespaces."""

################################################################################
#                          Python Installation Schemes                         #
################################################################################

STDLIB_MODULES = _enumerate_modules(get_paths()['stdlib'])
"""Standard Python library modules that are not platform-specific."""

PLATSTDLIB_MODULES = _enumerate_modules(get_paths()['platstdlib'])
"""Standard Python library modules that are platform-specific."""

PLATLIB_MODULES = _enumerate_modules(get_paths()['platlib'])
"""External Python packages that are site-specific and platform-specific."""

PURELIB_MODULES = _enumerate_modules(get_paths()['purelib'])
"""External Python packages that are site-specific but not platform-specific."""

################################################################################
#                            Python Module Sources                             #
################################################################################

BUILTIN_MODULES = set(builtin_module_names)
"""Set of all Python built-in modules."""

PYTHON_MODULES = BUILTIN_MODULES | PLATSTDLIB_MODULES | STDLIB_MODULES
"""Set of all Python built-in and stdlib python modules."""

EXTERNAL_MODULES = PLATLIB_MODULES | PURELIB_MODULES
"""Set of all external python modules in the current virtenv."""


__all__ = [
  # Constants (12)
  "PROJECT_ENTRYPOINT",
  "PROJECT_ROOT",
  "PROJECT_DOCS",
  "PROJECT_EXAMPLES",
  "PROJECT_NAMESPACES",
  "STDLIB_MODULES",
  "PLATSTDLIB_MODULES",
  "PLATLIB_MODULES",
  "PURELIB_MODULES",
  "BUILTIN_MODULES",
  "PYTHON_MODULES",
  "EXTERNAL_MODULES"
]
