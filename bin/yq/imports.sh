#!/usr/bin/env bash
# shellcheck disable=SC2086,SC2155

## @file
# Import management for vendored binaries
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##


case "$OSTYPE" in
  darwin*) yq_bin='yq_darwin_amd64' ;; 
  linux*)  yq_bin='yq_linux_amd64' ;;
  msys*)   yq_bin='yq_windows_amd64' ;;
esac

export yq=$(realpath ./bin/yq/$yq_bin)

# YQ_RELEASE="https://github.com/mikefarah/yq/releases/download/v4.30.8"
# mkdir -p ${yq%/*} && curl -o $yq -sL "$YQ_RELEASE/${yq##*/}" > /dev/null 2>&1
# chmod +x $yq