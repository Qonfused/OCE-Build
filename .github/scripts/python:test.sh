#!/usr/bin/env bash
#shellcheck disable=SC1091,SC2164

## @file
# Version matching script for Dortania or Github sources
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

# Change CWD for imports
__PWD__="$(pwd)"; cd "$(realpath "$(dirname "${BASH_SOURCE[0]}")/../../")"


pipenv shell

echo -e "\nAnalyzing tests..."
DATA_FILE="${$COVERAGE_FILE:-'.coverage'}"
coverage run -m --data-file="$DATA_FILE" pytest -v || exit 1

echo -e "\nCoverage report:"
coverage report -m --data-file="$DATA_FILE" --skip-covered

coverage html -d ".github/tmp/html" --data-file="$DATA_FILE" > /dev/null
echo -e "\nWrote HTML report to .github/tmp/html/index.html"
