#pragma no-implicit

## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Commands used for the OCE-Build CLI"""

from .build import cli as build_command
from .lock import cli as lock_command
from .patch import cli as patch_command

cli_commands = [
  build_command,
  lock_command,
  patch_command,
]
"""The list of commands to register with the CLI."""
