#!/usr/bin/env bash

## @file
# Apple plist parsing macros written in bash.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##


################################################################################
#                               Internal Methods                               #
################################################################################

__paired_key__() { sed -n "/^$2<$3>$/,/^$2<\/$3>$/p; /^$2<\/$3>$/q" <<< "$1"; }

__key_idx__() { grep -n -m 1 "<key>$2</key>" <<< "$1" | sed 's|\([0-9]*\).*|\1|'; }

__key__() {
  src="$1"; key="$2"
  # Key property match
  key_match=$(grep -m 1 "<key>$key</key>" <<< "$src")
  if [[ -z $key_match ]]; then return; fi
  s=$(sed -E 's|^([[:space:]]+).*|\1|' <<< "$key_match")
  # Get initial match
  value_match=$(grep -m 1 -A1 "$key_match" <<< "$src" | tail -n -1)
  type=$(awk -F'[<>]' '{print $2}' <<< "$value_match")
  # Handle boolean types
  if [[ "$value_match" == "$s<$type>" && $type == */ ]]; then
    type='boolean'
  # Handle multi-line matches
  elif [[ "$value_match" != "$s<$type>"*"</$type>" ]]; then
    offset=$(grep -n -m 1 "$key_match" <<< "$src" | sed 's|\([0-9]*\).*|\1|')
    src=$(tail -n +$offset <<< "$src")
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

################################################################################
#                                Plist Methods                                 #
################################################################################

remove_comments() {
  grep "<key>#.*</key>" <<< "$(cat "$1")" | while read ln; do
    idx=$(grep -n -m 1 "$ln" <<< "$(cat "$1")" | sed 's/\([0-9]*\).*/\1/')
    sed -i '' -e "$(($idx)),$(($idx+1))d" "$1" > /dev/null 2>&1
  done
}

replace_entries() {
  src="$(cat $1)"; set -f; keys=$(sed 's/\./\n/g' <<< "$2"); entries="$3"
  idx=0; while read -r key; do
    ((idx+="$(__key_idx__ "$src" "$key")"+0))
    src="$(__key__ "$src" "$key")"
  done <<< "$keys"

  s=$(head -n 1 <<< "$src" | sed -E 's/^([[:space:]]+).*/\1/')
  entries=$(sed -e "s|^|$s|" <<< "$entries" | awk '{printf "%s\\n", $0}')
  output=$(sed -e "$((idx+1)),$((idx+$(wc -l <<< "$src")))d" "$1"\
    | sed "${idx}s|$|\\n${entries}|"\
    | grep -Ev "^$")

  echo "$output" > "$1"
}

# Recursively adds missing entries, assuming dict type for each missing level.
recursive_add_entries() {
  src="$(cat "$1")"; tree=$(sed 's/\./\n/g' <<< "$2")
  idx=0; while read -r key; do
    val="$(__key__ "$src" "$key")"
    # Value exists
    if [[ -n $val ]]; then
      # Update cursor for next key
      ((idx+="$(__key_idx__ "$src" "$key")"+0)); src=$val
    # Value does not exist
    else
      # Handle creating new values
      s=$(head -n 1 <<< "$src" | sed -E 's/^([[:space:]]+).*/\1/')
      entry="$s\\t<key>$key<\/key>\\n$s\\t<dict>\\n$s\\t<\/dict>"
      # Add new entry
      idx="$((idx+$(wc -l <<< "$src")-1))"
      pl=$(sed "${idx}s|$|\\n$entry|" <<< "$(cat $1)" | grep -Ev "^$")
      echo "$pl" > "$1"
      # Update cursor for next key
      ((idx+=1)); src=$(__key__ "$(cat $1)" "$key")
    fi
  done <<< "$tree"
}

pq() {
  plist="$(cat $1)"; keys=$(sed 's/\./\n/g' <<< "$2")
  while read -r k; do
    key=$(sed -e 's/\[[^][]*\]//g' <<< "$k")
    plist="$(__key__ "$plist" "$key")"
    if [[ $k != $key ]]; then
      elem=$(echo "$k" | awk -F '[][]' '{print $2}')
      plist=$(__arr__ "$plist" $elem)
      if [[ -z "$elem" ]]; then plist=$(sed '1d;$d' <<< "$plist"); fi
    fi
  done <<< "$keys"
  echo "$plist"
}