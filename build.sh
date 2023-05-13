#!/usr/bin/env bash
#shellcheck disable=SC1091,SC2164

## @file
# OpenCore EFI build script
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

# Change CWD for imports
__PWD__=$(pwd); cd "$( dirname "${BASH_SOURCE[0]}" )"

source ./lib/config.sh

CONFIG=$(get_args "$(echo "$@")" '-c --config' 1)
if [[ -z "$CONFIG" || "$CONFIG" == "-c --config" ]]; then
  fexit "  Please provide a build config using the '-c' or '--config' flag.
  Example usage:
    \$ bash ./scripts/build.sh -c ../src/build.{json|yaml}"
elif [[ ! -f "$__PWD__/$CONFIG" ]]; then
  fexit "  Provided build config does not exist."
# Change config file reference to PWD
else CONFIG="$(realpath "$__PWD__/$CONFIG")"; fi

source ./lib/constants.sh
source ./lib/macros.sh
source ./lib/patches.sh
source ./lib/plist.sh
source ./lib/sources.sh

# Change CWD for config.json
cd "${CONFIG%/*}" || exit 1

################################################################################
#                            Prepare build folder                              #
################################################################################

# Create new build folder
rm -fr "$BUILD_DIR" > /dev/null 2>&1
mkdir -p "$BUILD_DIR"

# Create build lockfile
echo "
# This file is generated by running \"oce-build\" inside your project.
# Manual changes might be lost - proceed with caution!
" > "$LOCKFILE"

# Match to OC-pkg
OC_PKG=$(dBuild_pkg 'OpenCorePkg' "$OC_VERSION")
# Create OC-pkg resource folder
#shellcheck disable=SC2154
OC_LOCK=$($yq '.resolution' <<< "$OC_PKG")
OC_PKG_DIR="$BUILD_DIR"/.temp/${OC_LOCK%/*}/OpenCorePkg
mkdir -p "$OC_PKG_DIR"
# Unpackage OC-pkg source
OC_PKG_URL=$($yq '.url' <<< "$OC_PKG")
curl -sL "$OC_PKG_URL" | bsdtar -xvf- -C "$OC_PKG_DIR" > /dev/null 2>&1
# Update lockfile
entry=$($yq -n ".\"OpenCorePkg\" = $OC_PKG | with(.\"OpenCorePkg\" ;
  .extract = \"./X64/EFI/.\" |
  .type = \"directory\"
)" >> "$LOCKFILE")

# Create OC-bin resource folder
OC_BIN_DIR="$BUILD_DIR"/.temp/@acidanthera/OcBinaryData
mkdir -p "$OC_BIN_DIR"
# Sparse checkout OC-bin repo
git clone --filter=blob:none --sparse "$OC_BIN_URL" "$OC_BIN_DIR" > /dev/null 2>&1
git -C "$OC_BIN_DIR" sparse-checkout add "Drivers" > /dev/null 2>&1
git -C "$OC_BIN_DIR" sparse-checkout add "Resources" > /dev/null 2>&1
# Update lockfile
OC_BIN_SHA=$(git -C "$OC_BIN_DIR" rev-parse HEAD)
entry=$($yq -i e "with(.\"OpenCorePkg\" ;
  .dependencies.\"OcBinaryData\" |= {
    \"resolution\": \"@acidanthera/OcBinaryData@github:#${OC_BIN_SHA:0:8}\",
    \"url\": \"$OC_BIN_URL\",
    \"extract\": [\"./Drivers/.\", \"./Resources/.\"],
    \"type\": \"binary\"
  }
)" "$LOCKFILE")

# Extract OC scripts into scripts directory
mkdir -p "$SCR_DIR"/ocvalidate
cp -a "$OC_PKG_DIR"/Utilities/ocvalidate/. "$SCR_DIR"/ocvalidate
chmod +x "$OCVALIDATE"
cp -a "$OC_PKG_DIR"/Utilities/macserial/. "$SCR_DIR"/macserial
chmod +x "$MACSERIAL"

# Extract EFI directory
mkdir -p "$EFI_DIR"
cp -a "$OC_PKG_DIR"/X64/EFI/. "$EFI_DIR"
cp "$OC_PKG_DIR"/Docs/Sample.plist "$EFI_DIR"/OC/config.plist
# Copy OC-bin drivers
cp -a "$OC_BIN_DIR"/Drivers/. "$EFI_DIR"/OC/Drivers
# Copy OC-bin resources
cp -a "$OC_BIN_DIR"/Resources/. "$EFI_DIR"/OC/Resources
# Handle removing wild-card exclusions
cfg 'exclude.wildcard[]' | while read -r f; do
  if [[ -z $(cfg "include.wildcard[] | select(. == \"$f\")") ]]; then
    find "$EFI_DIR" -type f -name "$f" -delete
  fi
done

# Cleanup OC-pkg directory
rm -r "$OC_PKG_DIR"
# Cleanup OC-bin directory
rm -fr "$OC_BIN_DIR"/.git
rm -r "$OC_BIN_DIR"

################################################################################
#                               Build ACPI folder                              #
################################################################################

if [[ "$OSTYPE" == "darwin"* ]]; then
  # Create iasl directory
  IASL_DIR="$BUILD_DIR"/.temp/@acidanthera/MaciASL
  mkdir -p "$IASL_DIR"
  # Sparse checkout MaciASL repo
  git clone --filter=blob:none --sparse "$MACIASL_URL" "$IASL_DIR" > /dev/null 2>&1
  git -C "$IASL_DIR" sparse-checkout add "Dist" > /dev/null 2>&1
  # Copy iasl binary
  mkdir -p "$SCR_DIR"/bin
  cp "$IASL_DIR"/Dist/iasl-stable "$SCR_DIR"/bin/
  chmod +x "$IASL"
  # Cleanup MaciASL/iasl directory
  rm -fr "$IASL_DIR"/.git
  rm -r "$IASL_DIR"
elif ! IASL="$(type -p "iasl")" || [[ -z $IASL ]]; then
  fexit "No iasl executable or alias was found (e.g. in /usr/bin/iasl)."
fi

# Create ACPI resources folder
cfg 'include.acpi | keys | .[]' | while read -r ssdt; do
  if [[ -z "$ssdt" || -d "$ACPI_DIR/$ssdt.aml" ]]; then continue; fi

  src=$(cfg "include.acpi.\"$ssdt\"")
  target=$ACPI_DIR/$ssdt.aml

  # Build SSDT
  $IASL -ve -p "$target" "$src" > /dev/null 2>&1
done

# TODO: Handle building external ACPI sources and patches per ACPI spec

################################################################################
#                        Build Tools and Drivers folders                       #
################################################################################

# Remove non-whitelisted drivers and tools
#shellcheck disable=SC1087
for p in "$EFI_DIR"/OC/*/*.efi; do
  f=$(basename "${p%.*}")
  type=$(__lower__ "$(dirname "${p##*"$EFI_DIR"/OC/}")")
  case $type in
    drivers) DEFAULT='["OpenRuntime"]' ;;
    tools)   DEFAULT='["OpenShell"]'   ;;
  esac
  if [[ $DEFAULT == *"\"$f\""* ]]; then continue; fi
  
  INCLUDE=$(cfg "include.$type[] | select(. == \"$f\")")
  EXCLUDE=$(cfg "exclude.$type[] | select(. == \"$f\")")
  if [[ -z $INCLUDE || -n $EXCLUDE ]]; then rm "$p"; fi
done

################################################################################
#                              Build Kexts folder                              #
################################################################################

# Create and extract kext resources folder
cfg 'include.kexts | keys | .[]' | while read -r key; do
  if [[ -z "$key" || -d "$KEXTS_DIR/$key.kext" ]]; then continue; fi
  
  specifier=$(cfg "include.kexts.\"$key\"".specifier)
  # Fall back to actual key value if 'specifier' key does not exist
  if [[ -z $specifier ]]; then specifier=$(cfg "include.kexts.\"$key\""); fi
  # Handle kext if specifier matches a local filepath
  if [ -d "$specifier" ]; then cp -r "$specifier" "$KEXTS_DIR/$key.kext"; continue
  # Omit kext if packaged with another kext (or is a plugin)
  elif [[ $key == *"/"* || $specifier == "*" ]]; then continue; fi

  # Check that repo name (optional) matches kext name
  repo=$(echo "$specifier" | sed -E 's/.*\/([^:]+)=.*/\1/')
  kext=$([[ $specifier != "$repo" ]] && echo "$repo" || echo "$key")
  # Handle acidanthera kexts through dortania build repo
  if [[ $specifier != *"/"*"="* || $specifier == "acidanthera/"* ]]; then
    kext_pkg=$(dBuild_pkg "$kext" "${specifier#*=}")
  # Handle 3rd-party or unbuilt kexts through Github releases api
  else
    kext_pkg=$(Github_pkg "$key" "$kext" "$specifier")
  fi

  # Get version lock
  lock=$($yq '.resolution' <<< "$kext_pkg")
  if [[ -z "$lock" || $lock == 'null' ]]; then continue; fi
  # Download kext archive
  pdir=$BUILD_DIR/.temp/"${lock%/*}"
  pkg="$pdir/$kext"
  url=$($yq '.url' <<< "$kext_pkg")
  mkdir -p "$pkg" && curl -sL "$url" | bsdtar -xvf- -C "$pkg" > /dev/null 2>&1

  # Extract kext if only packaged binary
  match=$(find "$pkg" -maxdepth 3 -type d -name "*.kext")
  num=$(wc -l <<< "$match")
  if [[ $num -gt 1 ]]; then
    match=$(find "$pkg" -maxdepth 3 -name "$key.kext" | head -n 1)
  fi
  # Copy kext to EFI folder
  if [[ -n "$match" ]]; then cp -r "$match" "$KEXTS_DIR/$key.kext"; rm -r "$match"
  else rm -r "$pkg" >/dev/null 2>&1; continue; fi

  # Update lockfile
  entry=$($yq -n ".\"$key\" = $kext_pkg | with(.\"$key\" ;
    .extract = \".${match#*"$pkg"}\" |
    .type = \"kext\"
  )" >> "$LOCKFILE")
  
  # Extract bundled kexts
  find "$pkg" -maxdepth 3 -type d -name "*.kext" | while read -r p; do
    # Get kext entry
    k=$(basename "${p%.kext}")
    if [[ -z "$k" || -d "$KEXTS_DIR/$k.kext" ]]; then continue; fi
    # Get entry specifier
    s=$(cfg "include.kexts.\"$k\".specifier")
    if [[ -z $s ]]; then s=$(cfg "include.kexts.\"$k\""); fi
    # Extract kext if bundled or matches same specifier
    if [[ $s == '*' || $s == "$specifier" ]]; then
      cp -r "$p" "$KEXTS_DIR/$k.kext"; rm -r "$p"
      # Update lockfile
      $yq -i e "(.[] | select(.resolution == \"$lock\")).bundled
        .\"$k\" = { \"extract\": \".${p#*"$pkg"}\", \"type\": \"kext\" }"\
        "$LOCKFILE"
    fi
  done

  # Cleanup pkg
  rm -r "$pkg"
  # Cleanup parent package folder
  if [[ -z $(ls -A "$pdir") ]]; then rm -r "$pdir"; fi
done

################################################################################
#                             Build config.plist                               #
################################################################################

target="$EFI_DIR"/OC/config.plist

# Default to provided config.plist if provided
if [[ -f config.plist ]]; then cp config.plist "$target"
# Build config.plist if not provided
elif [[ ! -f config.yml ]]; then
  fexit "  Missing reference config.plist or config.yml file.
  Please provide a config.plist or config.yml file in the same directory as your build.yml file."
else
  # Default to OC Sample plist as template
  remove_comments "$target"

  SRC="$(cat config.yml)"
  # Parse additional config.plist patches based on script flags.
  PATCHES=(config.patch:*.yml)
  if [[ $PATCHES != 'config.patch:*.yml' ]]; then
    for i in "${!PATCHES[@]}"; do
      file="${PATCHES[i]}"
      patch="$(sed -e "s/config\.patch\:\(.*\)\.yml/\1/" <<< "$file")"
      if printf '%s\n' "$@" | grep -Fxq -- "--$patch"; then
        SRC+="$(echo -e "\n$(cat $file)")"
      fi
    done
  fi

  # Build each property specified in a config.yml file
  $yq -o=props --unwrapScalar=false <<< "$SRC" | while read -r ln; do
    # Skip over linebreaks or comments
    if [[ -z $ln || ${ln:0:1} == '#' ]]; then continue; fi

    # Handle build macros for conditional config.plist settings
    if [[ $ln =~ '@'(ifdef|endif).* ]]; then
      def=$(xargs <<< "${ln#*=}")
      case "$def" in
        'RELEASE'|'DEBUG') if [[ $def != "$OC_BUILD" ]]; then ((LN_SKIP=1)); fi ;;
        *) unset LN_SKIP ;;
      esac
    fi
    # Bail on macros after parsing and when set to skip lines
    if [[ ${ln:0:1} == '@' || $LN_SKIP ]]; then continue; fi

    # Skip over keys enforcing a strict entry schema
    keys=$(__trim__ "${ln%%=*}")
    if [[ $keys =~ ^ACPI.(Add|Delete|Patch)\..* \
      || $keys =~ ^Booter.(MmioWhitelist|Patch)\..* \
      || $keys =~ ^Kernel.(Add|Block|Force|Patch)\..* \
      || $keys =~ ^Misc.(Entries|Tools)\..* \
      || $keys =~ ^UEFI.(Drivers|ReservedMemory)\..* \
    ]]; then continue; fi

    # Recursively add missing entries
    entry=$(pq "$target" "$keys")
    if [[ -z $entry ]]; then recursive_add_entries "$target" "$keys"; fi

    # Parse macros and value types
    type=$(__trim__ "$(sed 's/.*\"\(.*\)|.*/\1/' <<< "$ln")")
    case $type in
      Macro)
        value=$(sed 's/.*| \(.*\)\".*/\1/' <<< "$ln")
        case $value in
          @Clear)
            # Skip null entries
            if [[ -z $entry ]]; then continue
            # Handle single-line entry
            elif [[ $(wc -l <<< "$entry") -lt 2 ]]; then
              output=$(grep -o '<[^>]*>' <<< "$value" | sed "N;s/\n//")
            # Handle multi-line entries
            else
              output=$(sed -n '1p;$p' <<< "$entry" | awk '{$1=$1};1')
            fi
          ;;
        esac
        ;;
      Data) output="<data>$(__parse_type__ "$ln")</data>" ;;
      String) output="<string>$(__parse_type__ "$ln")</string>" ;;
      Number) output="<integer>$(__parse_type__ "$ln")</integer>" ;;
      Boolean) output="<$(__parse_type__ "$ln")/>" ;;
    esac

    replace_entries "$target" "$keys" "$output"
  done
fi

mkdir -p "$BUILD_DIR"/.patches

# Build patches
build_acpi_patches
build_driver_patches
build_kext_patches
build_tool_patches

# Apply all patches to config.plist
replace_entries "$target" "ACPI.Add" "$ACPI_ADD"
replace_entries "$target" "ACPI.Patch" "$ACPI_PATCH"
replace_entries "$target" "Kernel.Add" "$KERNEL_ADD"
replace_entries "$target" "UEFI.Drivers" "$DRIVERS_ADD"
replace_entries "$target" "Misc.Tools" "$TOOLS_ADD"

################################################################################
#                                 Post-build                                   #
################################################################################

# Cleanup temp resources folder
rm -r "$BUILD_DIR"/.temp
rm -r "$BUILD_DIR"/.patches