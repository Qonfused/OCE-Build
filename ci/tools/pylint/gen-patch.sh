#!/usr/bin/env bash
#shellcheck disable=SC1091,SC2164

## @file
# Generates a patch file for pylintrc from the Google pylint config.
#
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

# Change CWD for imports
__PWD__=$(pwd); cd "$( dirname "${BASH_SOURCE[0]}" )"

# Generate patch
git diff --patch --no-index pylintrc-google .pylintrc > pylintrc.patch
