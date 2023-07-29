#pragma no-implicit

## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Portable OpenCore EFI dependency & build manager."""

from ocebuild.constants import *
from ocebuild.version import *

# Override the Python module search path to include third-party dependencies.
from third_party import inject_module
