#!/usr/bin/env bash

## @file
# Downloads and executes a binary release of the OCE Build CLI.
#
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

OCEBUILD_URL="https://github.com/Qonfused/OCE-Build"
OCEBUILD_VERSION="nightly"

#region Shell Macros

os() {
  if   [[ "$OSTYPE" == "msys" ]]; then
    echo "windows"
  elif [[ "$OSTYPE" == "linux"* ]]; then
    if [[ $(grep -i Microsoft /proc/version 2>/dev/null) ]]; then
      echo "windows" # running in WSL
    else
      echo "linux"
    fi
  elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "macos"
  fi
}

ext() {
  case $(os) in
    windows*) echo "$1.exe";;
    linux*)   echo "$1.linux";;
    macos*)   echo "$1";;
  esac
}

cmd() {
  [[ $(os) == "windows" ]] && echo "$1.exe" || echo "$1"
}

#endregion

# Arrange for the binary to be deleted when the script terminates
BINARY_PATH="./$(ext ocebuild)"
trap 'rm -f "$BINARY_PATH" 2>/dev/null' 0
trap 'exit $?' 1 2 3 15

# Download the binary release for the current platform
BINARY_URL="$OCEBUILD_URL/releases/download/$OCEBUILD_VERSION/$(ext ocebuild)"
$(cmd curl) -sSL -k $BINARY_URL > "$BINARY_PATH"

# Executes OCE Build with provided arguments
if [[ $(os) != "windows" ]]; then chmod +x "$BINARY_PATH"; fi
$BINARY_PATH "$@"
