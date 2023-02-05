#!/usr/bin/env bash

## @file
# Apple plist parsing macros written in bash.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##


__paired_key__() { sed -n "/^$2<$3>$/,/^$2<\/$3>$/p; /^$2<\/$3>$/q" <<< "$1"; }

__key__() {
  src="$1"; key="$2"
  # Key property match
  key_match=$(grep -m 1 "<key>$key</key>" <<< "$src")
  s=$(sed -E 's/^([[:space:]]+).*/\1/' <<< "$key_match")
  # Get initial match
  value_match=$(grep -m 1 -A1 "$key_match" <<< "$src" | tail -n -1)
  type=$(awk -F'[<>]' '{print $2}' <<< "$value_match")
  # Handle multi-line matches
  if [[ "$value_match" != "$s<$type>"*"</$type>" ]]; then
    src=$(awk "/$s<key>$key<\/key>/ ? c++ : c" <<< "$src")
    value_match=$(__paired_key__ "$src" "$s" "$type")
  fi
  # Return value match
  echo "$value_match"
}

__arr__() {
  src="$1"; elem=$(($2+0))
  # Match nearest array type
  key_match=$(grep -m 1 "<array>" <<< "$src")
  s=$(sed -E 's/^([[:space:]]+).*/\1/' <<< "$key_match")
  src=$(awk "/$s<array>/ ? c++ : c" <<< "$src")
  value_match=$(__paired_key__ "$src" "$s" "array")
  # Get nth element (if specified)
  if [[ -n "$2" ]]; then
    src=$(sed '1d;$d' <<< "$src");
    e=-1; while [[ $e -lt $elem ]]; do
      s=$(head -n 1 <<< "$src" | sed -E 's/^([[:space:]]+).*/\1/')
      type=$(head -n 1 <<< "$src" | grep -o '<[^>]*>' | tr -d "<>")
      value_match=$(__paired_key__ "$src" "$s" "$type")
      if [[ $(tail -n -1 <<< "$value_match") =~ ^"$s</$type>" ]]; then
        ((e++)); if [[ $e -eq $elem ]]; then break; fi
        # Exclude selection from next iteration
        src=$(tail -n +$(($(wc -l <<< "$value_match")+1)) <<< "$src");
      fi
    done
  fi
  echo "$value_match"
}

pq() {
  plist="$1";
  set -f; keys=($(echo ${2//./ }))
  for k in "${keys[@]}"; do
    key=$(sed -e 's/\[[^][]*\]//g' <<< "$k")
    plist="$(__key__ "$plist" "$key")"
    if [[ $k != $key ]]; then
      elem=$(echo "$k" | awk -F '[][]' '{print $2}')
      plist=$(__arr__ "$plist" $elem)
      if [[ -z "$elem" ]]; then plist=$(sed '1d;$d' <<< "$plist"); fi
    fi
  done
  echo "$plist"
}