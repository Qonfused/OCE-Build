#!/usr/bin/env bash

## @file
# JSON configuration reader script
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

source ./bin/yq/imports.sh
source ./lib/macros.sh


CONFIG=$(get_args "$@" '-c --config' "$(rsearch 'build.yml')")
if [[ -z "$CONFIG" || "$CONFIG" == "-c --config" ]]; then
  fexit "  Please provide a build config using the '-c' or '--config' flag.
  Example usage:
    \$ bash ./scripts/build.sh -c ../src/build.{json|yaml}"
elif [[ ! -f "$__PWD__/$CONFIG" ]]; then
  fexit "  Provided build config does not exist."
# Change config file reference to PWD
else CONFIG="$(realpath "$__PWD__/$CONFIG")"; fi

cfg() {
  src="$(cat $CONFIG | sed 's/".":/"wildcard":/')"
  # Default to regular json/yaml parsing
  output=$(sed '1{/^---$/!q;};1,/^---$/d' <<< "$src" | $yq ".$1")
  # Fall back to parsing yaml front-matter
  if [[ -z $output || $output == 'null' ]]; then
    output=$($yq --front-matter=extract ".$1" <<< "$src")
  fi
  [[ $output != 'null' ]] && echo "${output:-"$2"}" || echo "$2"
}