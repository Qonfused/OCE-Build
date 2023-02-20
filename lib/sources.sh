#!/usr/bin/env bash

## @file
# Version matching script for Dortania or Github sources
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

source ./bin/jq/imports.sh
source ./lib/constants.sh
source ./lib/macros.sh


# Inline Dortania build catalog
kCatalog=$(curl -sL $DORTANIA_BUILD_CATALOG)

# Get build url from Dortania build repo
dBuild_pkg() {
  entry=$($jq -r ".$1.versions" <<< "$kCatalog")
  build=$(__lower__ $OC_BUILD)
  nth_url() { $jq -r ".[$1].links.$build" <<< "$entry"; }
  nth_version() { $jq -r ".[$1].version" <<< "$entry"; }
  nth_commit() { $jq -r ".[$1].commit.sha[0:7]" <<< "$entry"; }
  i=0; case "$2" in
    latest*) ;; earliest*) ((i--));;
   *\#*) while [[ $(nth_commit $i) != "${2#*\#}" ]]; do ((i++)); done ;;
    \~*) while [[ $(nth_version $i) != "${2:1:3}" ]]; do ((i++)); done ;;
    \^*) while [[ $(nth_version $i) != "${2:1:1}"* ]]; do ((i++)); done ;;
      *) while [[ -n "$2" && $(nth_version $i) != "$2" ]]; do ((i++)); done ;;
  esac;
  url=$(nth_url $i); if [[ $url != 'null' ]]; then
    tree_url=$($jq -r ".[$i].commit.tree_url" <<< "$entry")
    src=$(sed -E 's/.*github.com\/([^:]+)\/tree.*/\1/' <<< "$tree_url")
    echo \
"{
  \"version\": \"$(nth_version $i)\",
  \"url\": \"$url\",
  \"resolution\": \"@$src@github:$(nth_version $i)#$(nth_commit $i)\",
  \"checksum\": \"$($jq -r ".[$i].hashes.$build.sha256" <<< "$entry")\"
}"
  fi
}

Github_pkg() {
  key=$1; bin=$2; src="${3%%=*}"
  # Fetch github releases api
  if [[ -n $GH_TOKEN ]]; then
    releases=$(curl -s \
      --request GET \
      --url https://api.github.com/repos/$src/releases \
      --header "Authorization: Bearer $GH_TOKEN")
  else
    releases=$(curl -s "https://api.github.com/repos/$src/releases")
  fi
  # Handle bad API requests
  if [[ $releases == *'Bad credentials'* || \
        $releases == *'API rate limit exceeded'*
  ]]; then
    msg=$($jq '.message' <<< "$releases"); fexit "[Github API]: ${msg%%. *}.\""
  fi
  # Parsing macros
  nth_pkg() {
    entry=$($jq ".[$1]" <<< "$releases")
    pkg=$($jq '.assets[0]' <<< "$entry")
    if [[ -n $pkg && $($jq '.assets[] | length' <<< "$entry") > 1 ]]; then
      query=$(sed 's/[-_]/.*/g' <<< "$bin-$OC_BUILD|$key")
      match=$($jq "first(.assets[] | select(.name|match(\"$query\")))" <<< "$entry")
      if [[ -n "$match" ]]; then pkg="$match"; fi
    fi; echo "$pkg";
  }
  nth_url() { $jq -r '.browser_download_url' <<< "$(nth_pkg $1)"; }
  nth_version() { $jq -r ".[$1].tag_name" <<< "$releases" | sed -e 's/[^0-9.]//g'; }
  i=0; v=${3#*=}; case "$v" in
    latest*) ;; earliest*) ((i--));;
    \~*) while [[ $(nth_version $i) != "${v:1:3}"* ]]; do ((i++)); done ;;
    \^*) while [[ $(nth_version $i) != "${v:1:1}"* ]]; do ((i++)); done ;;
      *) while [[ -n "$v" && $(nth_version $i) != "$v" ]]; do ((i++)); done ;;
  esac; url=$(nth_url $i); if [[ $url != 'null' ]]; then
    echo \
"{
  \"version\": \"$(nth_version $i)\",
  \"url\": \"$url\",
  \"resolution\": \"@$src@github:$(nth_version $i)#release\",
  \"checksum\": \"$(itr_checksum $url)\"
}"
  fi
}