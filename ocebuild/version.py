## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Contains the version string of OCE Build."""

# This project uses Semantic Versioning (https://semver.org/)
_MAJOR_VERSION = 0
_MINOR_VERSION = 0
_PATCH_VERSION = 0
_PRE_RELEASE   = 'dev'
_BUILD         = 0

# Export the OCE Build version string.
__version__    = '0.0.0-dev'
__all__        = ["__version__"] #pragma preserve-exports
