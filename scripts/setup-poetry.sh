#!/usr/bin/env bash

## @file
# Ensures that the local poetry environment is installed.
#
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

# Install project dependencies
poetry install -n

# Install global poetry plugins
poetry self add 'poethepoet[poetry_plugin]'   # Run poe tasks as `poetry <task>`

# Add pre-commit to git hooks
poetry run pre-commit install
