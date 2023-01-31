#!/usr/bin/env bash

## @file
# Version matching script for Dortania or Github sources
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

source ./lib/constants.sh


# Inline Dortania build catalog
kCatalog=$(curl -sL $DORTANIA_BUILD_CATALOG)

# Get build url from Dortania build repo
kBuild_pkg() {
  entry=$(echo "$kCatalog" | $jq -r ".$1.versions")
  nth_url() { echo "$entry" | $jq -r ".[$1].links.$(__lower__ $OC_BUILD)"; }
  nth_version() { echo "$entry" | $jq -r ".[$1].version"; }
  nth_commit() { echo "$entry" | $jq -r ".[$1].commit.sha[0:7]"; }
  i=0; case "$2" in
    latest*) ;; earliest*) ((i--));;
    *@*) while [[ $(nth_commit $i) != "${2#*@}" ]]; do ((i++)); done ;;
    \~*) while [[ $(nth_version $i) != "${2:1:3}" ]]; do ((i++)); done ;;
    \^*) while [[ $(nth_version $i) != "${2:1:1}"* ]]; do ((i++)); done ;;
      *) while [[ -n "$2" && $(nth_version $i) != "$2" ]]; do ((i++)); done ;;
  esac;
  url=$(nth_url $i); lock="$1-$(nth_version $i)@$(nth_commit $i)"
  [[ $url != 'null' ]] && echo "{\"url\": \"$url\", \"lock\": \"$lock\"}"
}

Github_pkg() {
  api_url="https://api.github.com/repos/${3%%=*}/releases"
  releases=$(curl -s "$api_url")
  key=$1; kext=$2; nth_pkg() {
    entry=$(echo "$releases" | $jq ".[$1]")
    pkg=$(echo "$entry" | $jq '.assets[0]')
    if [[ -z $pkg && $(echo "$entry" | $jq '.assets[] | length') > 1 ]]; then
      query=$(echo "$kext-$OC_BUILD|$key" | sed 's/[-_]/.*/g')
      pkg=$(echo "$entry" | $jq ".assets[] | select(.name|match(\"$query\"))")
    fi; echo "$pkg";
  }
  nth_url() { echo "$(nth_pkg $1)" | $jq -r '.browser_download_url'; }
  nth_version() { echo "$releases" | $jq -r ".[$1].tag_name" | sed -e 's/[^0-9.]//g'; }
  i=0; v=${3#*=}; case "$v" in
    latest*) ;; earliest*) ((i--));;
    # *@*) while [[ $(nth_commit $i) != "${2#*@}" ]]; do ((i++)); done ;;
    \~*) while [[ $(nth_version $i) != "${v:1:3}"* ]]; do ((i++)); done ;;
    \^*) while [[ $(nth_version $i) != "${v:1:1}"* ]]; do ((i++)); done ;;
      *) while [[ -n "$v" && $(nth_version $i) != "$v" ]]; do ((i++)); done ;;
  esac;
  url=$(nth_url $i); lock="$kext-$(nth_version $i)@release"
  [[ $url != 'null' ]] && echo "{\"url\": \"$url\", \"lock\": \"$lock\"}"
}