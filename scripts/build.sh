#!/usr/bin/env bash

## @file
# OpenCore EFI build script
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

source ./lib/config.sh
source ./lib/constants.sh
source ./lib/macros.sh
source ./lib/sources.sh


################################################################################
#                            Prepare build folder                              #
################################################################################

# Change CWD
cd "${CONFIG%/*}"

# Create new build folder
rm -r $BUILD_DIR > /dev/null 2>&1
mkdir -p $BUILD_DIR

# Match to OC-pkg
OC_PKG=$(kBuild_pkg 'OpenCorePkg' $OC_VERSION)
# Create OC-pkg resource folder
OC_LOCK=$(echo $OC_PKG | $jq -r '.resolution')
OC_PKG_DIR=$BUILD_DIR/.temp/$OC_LOCK
mkdir -p $OC_PKG_DIR
# Unpackage OC-pkg source
OC_PKG_URL=$(echo $OC_PKG | $jq -r '.url')
curl -sL $OC_PKG_URL | bsdtar -xvf- -C $OC_PKG_DIR > /dev/null 2>&1

# Extract EFI directory
mkdir -p $EFI_DIR
cp -a $OC_PKG_DIR/X64/EFI/. $EFI_DIR
# TODO: Handle removing wild-card exclusions
# for p in ("$(__arr__ $(cfg 'exclude."*"'))"); do
#   echo p $p
#   # INCLUDE=$(cfg $CONFIG "include.\*")
#   # EXCLUDE=$(cfg $CONFIG "exclude.\*")
#   # if [[ $INCLUDE != *"\"$p\""* && $EXCLUDE == *"\"$p\""* ]]; then
#   #   find $EFI_DIR -type f -name $p -delete
#   # fi
# done

# Create OC-bin resource folder
OC_BIN_DIR=$BUILD_DIR/.temp/@acidanthera/OcBinaryData
mkdir -p $OC_BIN_DIR
# Sparse checkout OC-bin repo
git clone --filter=blob:none --sparse $OC_BIN_URL $OC_BIN_DIR > /dev/null 2>&1
# Copy OC-bin drivers
git -C $OC_BIN_DIR sparse-checkout add "Drivers" > /dev/null 2>&1
cp -a $OC_BIN_DIR/Drivers/. $EFI_DIR/OC/Drivers
# Copy OC-bin resources
git -C $OC_BIN_DIR sparse-checkout add "Resources" > /dev/null 2>&1
cp -a $OC_BIN_DIR/Resources/. $EFI_DIR/OC/Resources
# Cleanup OC-bin directory
rm -fr $OC_BIN_DIR/.git
rm -r $OC_BIN_DIR

################################################################################
#                           Create Scripts directory                           #
################################################################################

mkdir -p $SCR_DIR/bin

# Extract OC scripts into scripts directory
cp -a $OC_PKG_DIR/Utilities/ocvalidate/ocvalidate $SCR_DIR/bin
# Mark ocvalidate as executable
chmod +x $OCVALIDATE

# Create iasl directory
IASL_DIR=$BUILD_DIR/.temp/@acidanthera/MaciASL
mkdir -p $IASL_DIR
# Sparse checkout MaciASL repo
git clone --filter=blob:none --sparse $MACIASL_URL $IASL_DIR > /dev/null 2>&1
git -C $IASL_DIR sparse-checkout add "Dist" > /dev/null 2>&1
# Copy iasl binary
cp $IASL_DIR/Dist/iasl-stable $SCR_DIR/bin/
# Mark iasl binary as executable
chmod +x $IASL
# Cleanup MaciASL/iasl directory
rm -fr $IASL_DIR/.git
rm -r $IASL_DIR

################################################################################
#                               Build ACPI folder                              #
################################################################################

# Create ACPI resources folder
cfg 'include.acpi' | $jq -r 'keys[]' | while read -r ssdt; do
  src=$(cfg "include.acpi.\"$ssdt\"")
  # Build SSDT
  target=$EFI_DIR/OC/ACPI/$ssdt.aml
  $IASL -ve -p "$target" "$src" > /dev/null 2>&1
done

# TODO: Handle building external ACPI sources and patches per ACPI spec

################################################################################
#                              Build Drivers folder                            #
################################################################################

# Remove non-whitelisted drivers
for p in $EFI_DIR/OC/Drivers/*.efi; do
  DEFAULT='["OpenRuntime"]'
  INCLUDE=$(cfg "include.drivers" $DEFAULT)
  EXCLUDE=$(cfg "exclude.drivers")
  f=$(basename ${p%.*})
  if [[ $INCLUDE != *"\"$f\""* || $EXCLUDE == *"\"$f\""* ]]; then rm $p; fi
done

################################################################################
#                              Build Kexts folder                              #
################################################################################

# Create and extract kext resources folder
cfg 'include.kexts' | $jq -r 'keys[]' | while read -r key; do
  if [[ -z "$key" || -d "$EFI_DIR/OC/Kexts/$key.kext" ]]; then continue; fi
  
  specifier=$(cfg "include.kexts.\"$key\"")
  # Handle kext if specifier matches a local filepath
  if [[ -d "$specifier" ]]; then
    cp -r "$specifier" $EFI_DIR/OC/Kexts/$key.kext; continue
  # Omit kext if packaged with another kext (or is a plugin)
  elif [[ $key == *"/"* || $specifier == "*" ]]; then continue; fi
  # Check that repo name (optional) matches kext name
  repo=$(echo "$specifier" | sed -E 's/.*\/([^:]+)=.*/\1/')
  kext=$([[ $specifier != $repo ]] && echo "$repo" || echo "$key")

  # Handle acidanthera kexts through dortania build repo
  if [[ $specifier != *"/"*"="* || $specifier == "acidanthera/"* ]]; then
    kext_pkg=$(kBuild_pkg $kext ${specifier#*=})
  # Handle 3rd-party or unbuilt kexts through Github releases api
  else
    kext_pkg=$(Github_pkg $key $kext $specifier)
  fi

  # Get version lock
  lock=$(echo "$kext_pkg" | $jq -r '.resolution | select( . != null )')
  if [[ -z "$lock" ]]; then continue; fi
  # Download kext archive
  pkg=$BUILD_DIR/.temp/$lock
  url=$(echo $kext_pkg | $jq -r '.url')
  mkdir -p $pkg && curl -sL $url | bsdtar -xvf- -C $pkg > /dev/null 2>&1

  # Extract kext if only packaged binary
  match=$(find $pkg -maxdepth 3 -type d -name "*.kext")
  num=$(echo "$match" | wc -l)
  if [[ $num -gt 1 ]]; then
    match=$(find $pkg -maxdepth 3 -type d -name "$key.kext")
  fi
  # Copy kext to EFI folder
  if [[ -n "$match" ]]; then cp -r "$match" $EFI_DIR/OC/Kexts/$key.kext; fi
done

# Extract bundled kexts from kext resources folder
cfg 'include.kexts' | $jq -r 'keys[]' | while read -r key; do
  if [[ -z "$key" || -d "$EFI_DIR/OC/Kexts/$key.kext" ]]; then continue; fi

  specifier=$(cfg "include.kexts.\"$key\"")
  # Omit kext if standalone or is a plugin
  if [[ $key == *"/"* || $specifier != "*" ]]; then continue; fi

  # Match existing packages to kext
  match=$(find $BUILD_DIR/.temp -maxdepth 4 -type d -name "${key##*/}.kext")
  if [[ -n "$match" ]]; then cp -r "$match" $EFI_DIR/OC/Kexts/$key.kext; fi
done

# Cleanup kext resources folder
rm -r $BUILD_DIR/.temp/kexts

################################################################################
#                             Build Tools folder                               #
################################################################################

# Remove non-whitelisted tools
for p in $EFI_DIR/OC/Tools/*.efi; do
  DEFAULT='["OpenShell"]'
  INCLUDE=$(cfg "include.tools" $DEFAULT)
  EXCLUDE=$(cfg "exclude.tools")
  f=$(basename ${p%.*})
  if [[ $INCLUDE != *"\"$f\""* || $EXCLUDE == *"\"$f\""* ]]; then rm $p; fi
done

################################################################################
#                             Build config.plist                               #
################################################################################

# Copy sample plist
cp $OC_PKG_DIR/Docs/Sample.plist $EFI_DIR/OC/config.plist
# Cleanup OC-pkg directory
rm -r $OC_PKG_DIR

# TODO