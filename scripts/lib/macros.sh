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

# Array manipulation
__arr__() {
  src=$(echo "${1//,/ }" | sed 's/[][]//g');
  echo "${src[@]%%,*}"
  # for i in "${src[@]%%,*}"; do echo "$i" | sed -En "s/\"([^\"]*).*/\\1/p"; done
}

# JSON manipulation
# __key__() { echo $1 | sed -En "s/\"([^\"]*).*/\\1/p"; }
# __value__() {
#   src="$1"
#   ln_match=$(echo "$src"\
#     | sed -En "s/.*\"$2\":(.*)/\\1/p"\
#     | awk '{gsub(/,$/,"");$1=$1};1')
#   case "$ln_match" in
#     \{*|\[*)
#       if [[ "${#ln_match}" -eq 1 ]]; then
#         read_ln() { echo "$src" | grep -we "\"$1\":" -A $2 | sed -n "$2p"; }
#         count() { ln=$(read_ln $1 $2); w="${ln/[^[:space:]]*/}"; echo "${#w}"; }
#         i=2; while [[ $(count $2 $i) -gt $(count $2 1) ]]; do ((i++)); done
#         echo "$src" | grep -we "\"$2\":" -A $i | sed -n "2,$(($i-1))p"
#       else
#         echo "C-1" $3
#         count() { idx=$1; echo "${ln_match:0:idx}" | grep -Eo "$2" | wc -l; }
#         if [[ $3=="--eol" ]]; then echo $ln_match;
#         else
#           [ "${ln_match:0:1}" == '{' ] && o='\{' && c='\}'
#           [ "${ln_match:0:1}" == '[' ] && o='\[' && c='\]'
#           echo $ln_match | sed -En "s/$o([^$o]*).*$c/\\1/p"
#           # TODO: handle inline json parsing
#           #i=2; while [[ $(count $i $o) != $(count $i $c) ]]; do ((i++)); done
#           #echo $i "${ln_match:0:i}"
#           #echo $(count $i $o) $(count $i $c)
#         fi
#       fi ;;
#     \"*) echo $ln_match | sed -En "s/\"([^\"]*).*/\\1/p" ;;
#     #\"*) echo $(__key__ $ln_match) ;;
#       *) echo $ln_match ;;
#   esac
# }