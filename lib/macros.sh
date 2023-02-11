#!/usr/bin/env bash

## @file
# A collection of macros for extending Bash functionality
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##


################################################################################
#                               Internal Macros                                #
################################################################################

# String manipulation
__lower__() { echo "$1" | tr "[:upper:]" "[:lower:]"; }
__upper__() { echo "$1" | tr "[:lower:]" "[:upper:]"; }
__trim__() { echo "${1//[[:space:]]/}"; }

# Array manipulation
__arr__() {
  src=$(echo "${1//,/ }" | sed 's/[][]//g');
  echo "${src[@]%%,*}"
  # for i in "${src[@]%%,*}"; do echo "$i" | sed -En "s/\"([^\"]*).*/\\1/p"; done
}

# Parse yaml/plist types
__parse__() {
  type=$(__trim__ $(sed 's/.*\"\(.*\)|.*/\1/' <<< "$1"))
  value=$(sed 's/.*| \(.*\)\".*/\1/' <<< "$1" | tr -d '\\"')
  case $type in
    Data) value=$(sed 's/.*<\(.*\)>.*/\1/' <<< "$value" | xxd -r -p | base64) ;;
    String) value=$(sed 's/.*\"\(.*\)\".*/\1/' <<< "$value") ;;
    *) value=$(sed 's/.*| \(.*\).*/\1/' <<< "$ln" | tr -d '\\"') ;;
  esac
  echo "$value"
}

################################################################################
#                                 Shell Macros                                 #
################################################################################

get_args() {
  args=($1); declare -a kargs=($2)
  for k in "${kargs[@]}"; do
    for i in "${!args[@]}"; do
      if [[ "${args[$i]}" = "${k}" ]]; then echo ${args[$(($i+1))]}; break; fi
    done
  done
  echo "$2"
}

fexit () { printf '%s\n' "$1" >&2; exit "${2-1}"; }

################################################################################
#                              Filesystem Macros                               #
################################################################################

rsearch() {
  # Ref: https://www.npmjs.com/package/find-config#algorithm
  if [ -f "$1" ]; then printf '%s\n' "${PWD%/}/$1"
  elif [ "$PWD" != / ]; then (cd .. && rsearch "$1")
  fi
}

################################################################################
#                              Networking Macros                               #
################################################################################

itr_checksum() {
  url=$1
  checksum() { curl -sL "$url" | shasum -a 256 | grep -o '^\S*'; }
  arr=($(for i in {1..3}; do checksum; done))
  IFS=$'\n' sort <<<"${arr[*]}" | uniq -d; unset IFS
}