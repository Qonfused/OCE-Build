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

# Parse yaml/plist types
__parse_type__() {
  type=$(__trim__ $(sed 's/.*\"\(.*\)|.*/\1/' <<< "$1"))
  value=$(sed 's/.*| \(.*\)\".*/\1/' <<< "$1" | sed 's/\\"/\"/g')
  case $type in
    Data) value=$(sed 's/.*<\(.*\)>.*/\1/' <<< "$value" | xxd -r -p | base64) ;;
    String)
      # Handle incorrect shell escaping
      if [[ "${value: -1}" != \" ]]; then value+=$'"'; fi
      value=$(sed 's/.*\"\(.*\)\".*/\1/' <<< "$value") ;;
    *) value=$(sed 's/.*| \(.*\).*/\1/' <<< "$ln" | tr -d '\\"') ;;
  esac
  echo "||$type|| $|$ ||$value||" >> ~/Desktop/diag.log
  echo "$value"
}

################################################################################
#                                 Shell Macros                                 #
################################################################################

get_args() {
  declare -a args=($1); declare -a kargs=($2)
  [[ -n $3 ]] && offset=$3 || offset=0;
  for k in "${kargs[@]}"; do
    i=-1; while (( i++ < "${#args[@]}" )); do
      if [[ "${args[$i]}" == "${k}" ]]; then
        echo ${args[$((i+offset))]}; break
      fi
    done
  done
}

fexit () { printf '%s\n' "$1" >&2; exit "${2-1}"; }

################################################################################
#                              Networking Macros                               #
################################################################################

itr_checksum() {
  url="$1"
  checksum() { curl -sL "$url" | shasum -a 256 | grep -Eo '[a-z0-9]+'; }
  arr=($(for i in {1..3}; do checksum; done))
  IFS=$'\n' sorted=($(sort <<<"${arr[*]}")); unset IFS
  echo "${sorted[0]}"
}