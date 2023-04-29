#!/usr/bin/env bash
#shellcheck disable=SC1091

## @file
# JSON configuration reader script
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

source ./bin/yq/imports.sh
source ./lib/macros.sh


################################################################################
#                               Internal Methods                               #
################################################################################

#shellcheck disable=SC2154
cfg() {
  src="$(cat "$CONFIG" | sed 's/".":/"wildcard":/')"
  # Default to regular json/yaml parsing
  output=$(sed '1{/^---$/!q;};1,/^---$/d' <<< "$src" | $yq ".$1")
  # Fall back to parsing yaml front-matter
  if [[ -z $output || $output == 'null' ]]; then
    output=$($yq --front-matter=extract ".$1" <<< "$src")
  fi
  [[ $output != 'null' ]] && echo "${output:-"$2"}" || echo "$2"
}