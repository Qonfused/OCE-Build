#!/usr/bin/env bash

## @file
# Outputs a rich formatted message from the command line.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

poetry run python3 -c "import rich; rich.get_console().print(\"$@\")"
