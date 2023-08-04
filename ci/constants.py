## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Constants used by the CI system."""

from sys import builtin_module_names
from sysconfig import get_paths

from third_party.cpython.pathlib import Path


def _enumerate_modules(path: str) -> set:
  """Returns a set of all modules in a directory."""
  files = set()
  for f in sorted(Path(path).iterdir()):
    name = f.stem
    if f.is_dir() and f.joinpath('__init__.py').exists():
      files.add(name)
    elif f.is_file() and f.suffix == '.py':
      files.add(name)

  return files

################################################################################
#                              Project Constants                               #
################################################################################

PROJECT_ENTRYPOINT = Path(__file__, '../' * 2, 'ocebuild').resolve()
"""The main project's import entrypoint."""

PROJECT_ROOT = PROJECT_ENTRYPOINT.parent
"""The project's root directory."""

PROJECT_DOCS = PROJECT_ROOT.joinpath('docs')
"""The project's documentation directory."""

PROJECT_EXAMPLES = PROJECT_ROOT.joinpath('examples')
"""The project's examples directory."""

PROJECT_NAMESPACES = _enumerate_modules(PROJECT_ROOT)
"""The project's root namespaces."""

PROJECT_BUILD_STAGING = PROJECT_ROOT.joinpath('ci/tools/poetry/staging')
"""The project's build staging directory."""

PROJECT_BUILD_PATHS = (
  PROJECT_ROOT.joinpath('ci/tools/poetry/build'),
  PROJECT_ROOT.joinpath('ci/tools/pyinstaller/build'),
  PROJECT_ROOT.joinpath('ci/tools/sphinx/api'),
  PROJECT_ROOT.joinpath('dist'),
  PROJECT_ROOT.joinpath('docs/build'),
  *PROJECT_ROOT.joinpath('examples').glob('**/dist'),
)
"""The project's temporary build directories."""

################################################################################
#                            Python Environment Checks                         #
################################################################################

IS_FULL_ENV = Path(PROJECT_ROOT, 'ci/tools/poetry/tasks.toml').exists()
"""Whether the current environment is a full development environment."""

HAS_RAN_HOOKS = Path('dist').exists() and not any(Path('dist').glob('*.whl'))
"""Whether the pre/post build hooks have been run."""

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
  # Constants (16)
  "PROJECT_ENTRYPOINT",
  "PROJECT_ROOT",
  "PROJECT_DOCS",
  "PROJECT_EXAMPLES",
  "PROJECT_NAMESPACES",
  "PROJECT_BUILD_STAGING",
  "PROJECT_BUILD_PATHS",
  "IS_FULL_ENV",
  "HAS_RAN_HOOKS",
  "STDLIB_MODULES",
  "PLATSTDLIB_MODULES",
  "PLATLIB_MODULES",
  "PURELIB_MODULES",
  "BUILTIN_MODULES",
  "PYTHON_MODULES",
  "EXTERNAL_MODULES"
]
