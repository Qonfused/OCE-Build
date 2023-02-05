#!/usr/bin/env bash

## @file
# Import management for vendored binaries
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##


case "$OSTYPE" in
  darwin*) jq_bin='jq-osx-amd64' ;; 
  linux*)  jq_bin='jq-linux64' ;;
  msys*)   jq_bin='jq-win64.exe' ;;
esac
jq=$(realpath ./bin/jq/$jq_bin)
# JQ_RELEASE="https://github.com/stedolan/jq/releases/download/jq-1.6"
# mkdir -p ${jq%/*} && curl -o $jq -sL "$JQ_RELEASE/${jq##*/}" > /dev/null 2>&1
# chmod +x $jq