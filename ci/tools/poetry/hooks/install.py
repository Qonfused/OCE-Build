#!/usr/bin/env python3

## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Poetry install hook for poetry-core."""

import subprocess

from typing import Set

from toml import load as toml_load

#pragma preserve-imports - Inject project namespaces into the module search path
import sys, pathlib; sys.path.insert(1, str(pathlib.Path(__file__, '../' * 5).resolve()))

from ci.constants import PROJECT_ROOT
from ci.constants import IS_FULL_ENV, HAS_RAN_HOOKS

from third_party.cpython.pathlib import Path


POSTINSTALL_CMDS = (
  'poetry run pre-commit install',
)

def get_poetry_plugins() -> Set[str]:
  out = subprocess.run(['poetry', 'self', 'show'],
                       capture_output = True,
                       text = True)
  plugins = list(map(lambda l: l.split(' ', maxsplit=1)[0],
                     out.stdout.split('\n')))

  return set(filter(lambda p: len(p), plugins))

def configure_project_plugins():
  # Configure Poetry plugins
  if (file := Path(PROJECT_ROOT, 'ci/tools/poetry/plugins.toml')).exists():
    plugins_dict = toml_load(file)
    pending_plugins = set(toml_load(file).keys()) - get_poetry_plugins()
    for resolver in map(lambda p: plugins_dict[p], pending_plugins):
      subprocess.run(['poetry', 'self', 'add', resolver])


def _main():
  if HAS_RAN_HOOKS or not IS_FULL_ENV:
    exit(0)
  elif IS_FULL_ENV:
    configure_project_plugins()
    for cmd in POSTINSTALL_CMDS:
      subprocess.run(cmd.split())

if __name__ == '__main__':
  _main()
