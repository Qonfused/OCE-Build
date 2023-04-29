#!/usr/bin/env bash
#shellcheck disable=SC1091,SC2155

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

export OC_VERSION="$(cfg '"oc-version"' "latest")"
export OC_BUILD="$(cfg '"oc-build"' "DEBUG")"
export OC_COMMIT="$(cfg '"oc-commit"')"
export BUILD_DIR="$(cfg "build_dir" "./dist")"

# Lock build_dir reference to PWD
export BUILD_DIR="$__PWD__/${BUILD_DIR##*/}"

################################################################################
#                              Hardcoded constants                             #
################################################################################

export OC_PKG_URL="https://github.com/acidanthera/OpenCorePkg/"
export OC_BIN_URL="https://github.com/acidanthera/OcBinaryData/"

export DORTANIA_BUILD_URL="https://github.com/dortania/build-repo/releases/download"
export DORTANIA_BUILD_CATALOG="https://raw.githubusercontent.com/dortania/build-repo/builds/config.json"

export GENSMBIOS_URL="https://github.com/corpnewt/GenSMBIOS"
export MACIASL_URL="https://github.com/acidanthera/MaciASL/"

################################################################################
#                                Build Resources                               #
################################################################################

export EFI_DIR="$BUILD_DIR"/EFI
export ACPI_DIR="$BUILD_DIR"/EFI/OC/ACPI
export KEXTS_DIR="$BUILD_DIR"/EFI/OC/Kexts

export SCR_DIR="$BUILD_DIR"/scripts
export LOCKFILE="./build.lock"

# Executables
OCVALIDATE="$SCR_DIR/ocvalidate/ocvalidate"
MACSERIAL="$SCR_DIR/macserial/macserial"
if [[ "$OSTYPE" != "darwin"* ]]; then
    OCVALIDATE+=".linux"
    MACSERIAL+=".linux"
fi
export OCVALIDATE
export MACSERIAL

IASL="$SCR_DIR/bin/iasl-stable"
if [[ "$OSTYPE" != "darwin"* ]]; then IASL="$(type -p "iasl")"; fi
export IASL