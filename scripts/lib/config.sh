#!/usr/bin/env bash

## @file
# JSON configuration reader script
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

source ./bin/jq/imports.sh
source ./lib/macros.sh


CONFIG=$(get_args "$@" '-c --config' "$(rsearch 'config.json')")

cfg() {
  output=$(cat "$CONFIG" | $jq -r ".$1 | select( . != null )" 2>/dev/null)
  [[ -n $output ]] && echo "$output" || echo "$2"
}