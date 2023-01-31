#!/usr/bin/env bash

## @file
# JSON configuration reader script
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##


SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

jq_bin=jq-$([[ $OSTYPE == darwin* ]] && echo "osx-amd64" || echo "linux64")
jq=$(realpath ./bin/jq/$jq_bin)
# JQ_RELEASE="https://github.com/stedolan/jq/releases/download/jq-1.6"
# mkdir -p ${jq%/*} && curl -o $jq -sL "$JQ_RELEASE/${jq##*/}" > /dev/null 2>&1
# chmod +x $jq

rsearch() {
  # Ref: https://www.npmjs.com/package/find-config#algorithm
  if [ -f "$1" ]; then printf '%s\n' "${PWD%/}/$1"
  elif [ "$PWD" != / ]; then (cd .. && rsearch "$1")
  fi
}

CONFIG=$(rsearch 'config.json')

cfg() {
  output=$(cat "$CONFIG" | $jq -r ".$1 | select( . != null )" 2>/dev/null)
  [[ -n $output ]] && echo "$output" || echo "$2"
}