#!/usr/bin/env bash

## @file
# Build constants
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

source ./lib/config.sh


################################################################################
#                            config.json properties                            #
################################################################################

OC_VERSION=$(cfg '"oc-version"' "latest")
OC_BUILD=$(cfg '"oc-build"' "DEBUG")
OC_COMMIT=$(cfg '"oc-commit"')
BUILD_DIR=$(cfg "build_dir" "./dist")

################################################################################
#                              Hardcoded constants                             #
################################################################################

OC_PKG_URL="https://github.com/acidanthera/OpenCorePkg/"
OC_BIN_URL="https://github.com/acidanthera/OcBinaryData/"
MACIASL_URL="https://github.com/acidanthera/MaciASL/"
DORTANIA_BUILD_URL="https://github.com/dortania/build-repo/releases/download"
DORTANIA_BUILD_CATALOG="https://raw.githubusercontent.com/dortania/build-repo/builds/config.json"

################################################################################
#                               Derived properties                             #
################################################################################

# Build resources
OC_PKG_DIR=$BUILD_DIR/.temp/OC-pkg
OC_BIN_DIR=$BUILD_DIR/.temp/OC-bin
IASL_DIR=$BUILD_DIR/.temp/iasl

SCR_DIR=$BUILD_DIR/scripts
EFI_DIR=$BUILD_DIR/EFI

# Executables
OCVALIDATE="$SCR_DIR/bin/ocvalidate"
IASL="$SCR_DIR/bin/iasl-stable"