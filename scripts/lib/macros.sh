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

# # Array manipulation
# __arr__() {
#   src=$(echo "${1//,/ }" | sed 's/[][]//g');
#   echo "${src[@]%%,*}"
#   # for i in "${src[@]%%,*}"; do echo "$i" | sed -En "s/\"([^\"]*).*/\\1/p"; done
# }

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

################################################################################
#                              Filesystem Macros                               #
################################################################################

rsearch() {
  # Ref: https://www.npmjs.com/package/find-config#algorithm
  if [ -f "$1" ]; then printf '%s\n' "${PWD%/}/$1"
  elif [ "$PWD" != / ]; then (cd .. && rsearch "$1")
  fi
}