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
if [[ -z "$CONFIG" || "$CONFIG" == "-c --config" ]]; then
  fexit "  Please provide a config filepath using the '-c' or '--config' flag.
  Example usage:
    \$ bash ./scripts/build.sh -c ../src/config.{json|yaml}"
elif [[ ! -f "$__PWD__/$CONFIG" ]]; then
  fexit "  Provided config filepath does not exist."
# Change config file reference to PWD
else CONFIG="$(realpath "$__PWD__/$CONFIG")"; fi

cfg() {
  output=$(cat "$CONFIG" | $jq -r ".$1 | select( . != null )" 2>/dev/null)
  [[ -n $output ]] && echo "$output" || echo "$2"
}