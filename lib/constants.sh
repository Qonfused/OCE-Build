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

# Lock build_dir reference to PWD
BUILD_DIR="$__PWD__/${BUILD_DIR##*/}"

################################################################################
#                              Hardcoded constants                             #
################################################################################

OC_PKG_URL="https://github.com/acidanthera/OpenCorePkg/"
OC_BIN_URL="https://github.com/acidanthera/OcBinaryData/"

DORTANIA_BUILD_URL="https://github.com/dortania/build-repo/releases/download"
DORTANIA_BUILD_CATALOG="https://raw.githubusercontent.com/dortania/build-repo/builds/config.json"

GENSMBIOS_URL="https://github.com/corpnewt/GenSMBIOS"
MACIASL_URL="https://github.com/acidanthera/MaciASL/"

################################################################################
#                                Build Resources                               #
################################################################################

EFI_DIR=$BUILD_DIR/EFI
ACPI_DIR=$BUILD_DIR/EFI/OC/ACPI
KEXTS_DIR=$BUILD_DIR/EFI/OC/Kexts

SCR_DIR=$BUILD_DIR/scripts
LOCKFILE="./build.lock"

# Executables
OCVALIDATE="$SCR_DIR/ocvalidate/ocvalidate"
MACSERIAL="$SCR_DIR/macserial/macserial"
if [[ "$OSTYPE" != "darwin"* ]]; then
    OCVALIDATE+=".linux"
    MACSERIAL+=".linux"
fi

IASL="$SCR_DIR/bin/iasl-stable"
if [[ "$OSTYPE" != "darwin"* ]]; then IASL="$(type -p "iasl")"; fi