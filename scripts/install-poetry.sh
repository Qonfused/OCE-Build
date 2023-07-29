#!/usr/bin/env bash

## @file
# Ensures that poetry is installed.
#
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

POETRY_URL="https://install.python-poetry.org"
POETRY_VERSION="1.5.0"
POETRY_ARGS="-y --version $POETRY_VERSION"

# Windows
if [[ "$OSTYPE" == "win32" ]]; then
  pwsh -command "(Invoke-WebRequest -Uri $POETRY_URL -UseBasicParsing).Content | py - $POETRY_ARGS"
# Linux and MacOS
else
  curl -sSL -k $POETRY_URL | python3 - $POETRY_ARGS
fi
