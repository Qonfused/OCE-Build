#!/usr/bin/env bash
#shellcheck disable=SC2154

## @file
# OpenCore config.plist patching macros written in bash.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

# REQUIRES ../bin/yq/imports.sh


################################################################################
#                                 ACPI Patches                                 #
################################################################################

ACPI_ADD=$'<array>\n</array>'
ACPI_ADD_ENTRY() {
  echo \
"  <dict>
    <key>Comment</key>
    <string>$1</string>
    <key>Enabled</key>
    <${2}/>
    <key>Path</key>
    <string>$3</string>
  </dict>"
}

ACPI_PATCH=$'<array>\n</array>'
ACPI_PATCH_ENTRY() {
  echo \
"  <dict>
    <key>Base</key>
    <string>$1</string>
    <key>BaseSkip</key>
    <integer>$2</integer>
    <key>Comment</key>
    <string>$3</string>
    <key>Count</key>
    <integer>$4</integer>
    <key>Enabled</key>
    <$5/>
    <key>Find</key>
    <data>$6</data>
    <key>Limit</key>
    <integer>$7</integer>
    <key>Mask</key>
    <data>$8</data>
    <key>OemTableId</key>
    <data>$9</data>
    <key>Replace</key>
    <data>${10}</data>
    <key>ReplaceMask</key>
    <data>${11}</data>
    <key>Skip</key>
    <integer>${12}</integer>
    <key>TableLength</key>
    <integer>${13}</integer>
    <key>TableSignature</key>
    <data>${14}</data>
  </dict>"
}

build_acpi_patches() {
  # Build '$.ACPI.Add' entries for all SSDTs
  cfg 'include.acpi | keys | .[]' | while read -r key; do
    if [[ -z "$key" && ! -d "$ACPI_DIR/$key.aml" ]]; then continue; fi

    # Build ACPI entry values
    Comment=$(cfg "include.acpi.\"$key\".Comment") #A
    Enabled=$(cfg "include.acpi.\"$key\".Enabled") #B
    Path=$(cfg "include.acpi.\"$key\".Path")       #C

    # Default ACPI entry values (placeholders)
    A="$key"
    B=$([[ -z $(cfg "exclude.acpi.$key") ]] && echo "true" || echo "false")
    C="$key.aml"

    # Append ACPI entry
    offset=$(($(wc -l <<< "$ACPI_ADD")-1))
    entry=$(awk '{printf "%s\\n", $0}'\
      <<< "$(ACPI_ADD_ENTRY "${Comment:-$A}" "${Enabled:-$B}" "${Path:-$C}")")
    ACPI_ADD=$(sed "${offset}s|$|\\n${entry}|" <<< "$ACPI_ADD" | grep -Ev "^$")

    # Create plist patch
    echo "$ACPI_ADD" > "$BUILD_DIR"/.patches/ACPI_ADD.plist
  done

  ACPI_ADD="$(cat "$BUILD_DIR"/.patches/ACPI_ADD.plist 2>/dev/null)"

  # Build '$.ACPI.Patch' entries for configured patches
  for ((i=0; i<$($yq '.ACPI.Patch | length' <<< "$(cat config.yml)"); i++)); do
    patch=$($yq --unwrapScalar=false ".ACPI.Patch.$i" <<< "$(cat config.yml)")

    get_key() {
      ln="$($yq --unwrapScalar=false ".\"$1\"" <<< "$patch")"
      if [[ -n $ln && $ln != 'null' ]]; then echo "$(__parse_type__ "$ln")"
      else echo "$2"; fi
    }

    # Build ACPI patch values
    Base=$(           get_key 'Base'            '')
    BaseSkip=$(       get_key 'BaseSkip'        '0')
    Comment=$(        get_key 'Comment'         '')
    Count=$(          get_key 'Count'           '0')
    Enabled=$(        get_key 'Enabled'         'true')
    Find=$(           get_key 'Find'            '')
    Limit=$(          get_key 'Limit'           '0')
    Mask=$(           get_key 'Mask'            '')
    OemTableId=$(     get_key 'OemTableId'      '')
    Replace=$(        get_key 'Replace'         '')
    ReplaceMask=$(    get_key 'ReplaceMask'     '')
    Skip=$(           get_key 'Skip'            '0')
    TableLength=$(    get_key 'TableLength'     '0')
    TableSignature=$( get_key 'TableSignature'  '')

    # Append ACPI entry
    offset=$(($(wc -l <<< "$ACPI_PATCH")-1))
    entry=$(awk '{printf "%s\\n", $0}'\
      <<< "$(ACPI_PATCH_ENTRY "$Base" "$BaseSkip" "$Comment" "$Count" "$Enabled" "$Find" "$Limit" "$Mask" "$OemTableId" "$Replace" "$ReplaceMask" "$Skip" "$TableLength" "$TableSignature")")

    ACPI_PATCH=$(sed "${offset}s|$|\\n${entry}|" <<< "$ACPI_PATCH" | grep -Ev "^$")

    # Create plist patch
    echo "$ACPI_PATCH" > "$BUILD_DIR"/.patches/ACPI_PATCH.plist
  done

  ACPI_PATCH="$(cat "$BUILD_DIR"/.patches/ACPI_PATCH.plist 2>/dev/null)"
}

################################################################################
#                                Driver Patches                                #
################################################################################

DRIVERS_ADD=$'<array>\n</array>'
DRIVER_ADD_ENTRY() {
  echo \
"  <dict>
    <key>Arguments</key>
    <string>$1</string>
    <key>Comment</key>
    <string>$2</string>
    <key>Enabled</key>
    <${3}/>
    <key>LoadEarly</key>
    <${4}/>
    <key>Path</key>
    <string>$5</string>
  </dict>"
}

build_driver_patches() {
  # Build '$.UEFI.Drivers' entries for all drivers
  cfg 'include.drivers[]' | while read -r key; do
    # if [[ -z "$key" && ! -d "$KEXTS_DIR/$key.kext" ]]; then continue; fi

    # Build Driver entry values
    Arguments=''
    Comment="$key"
    Enabled=$([[ -z $(cfg "exclude.drivers.$key") ]] && echo "true" || echo "false")
    LoadEarly='false'
    Path="$key.efi"

    # Handle 'LoadEarly' quirk with OpenRuntime and OpenVariableRuntime
    # @see https://github.com/acidanthera/OpenCorePkg/commit/14df4ad249dd7abf9f4d52fe8fd51122d58b96c7
    offset=$(($(wc -l <<< "$DRIVERS_ADD")-1))
    if [[ -n $(cfg "include.drivers[] | select(. == \"OpenVariableRuntimeDxe\")") ]]; then
      case $key in
      'OpenVariableRuntime')
        LoadEarly='true'
        # Get load index for OpenRuntime
        idx=$(cfg 'include.drivers[]' | grep -n 'OpenRuntime' | sed 's/\([0-9]*\).*/\1/')
        offset="$(($((idx-1))*$(wc -l <<< "$(TOOL_ENTRY)")))"
        ;;
      'OpenRuntime')
        LoadEarly='true'
        ;;
      esac
    fi

    # Append Driver entry
    entry=$(awk '{printf "%s\\n", $0}'\
      <<< "$(DRIVER_ADD_ENTRY "$Arguments" "$Comment" "$Enabled" "$LoadEarly" "$Path")")
    DRIVERS_ADD=$(sed "${offset}s|$|\\n${entry}|" <<< "$DRIVERS_ADD" | grep -Ev "^$")
    
    # Create plist patch
    echo "$DRIVERS_ADD" > "$BUILD_DIR"/.patches/DRIVERS_ADD.plist
  done

  DRIVERS_ADD="$(cat "$BUILD_DIR"/.patches/DRIVERS_ADD.plist 2>/dev/null)"
}

################################################################################
#                                 Kext Patches                                 #
################################################################################

KERNEL_ADD=$'<array>\n</array>'
KEXT_ADD_ENTRY() {
  echo \
"  <dict>
    <key>Arch</key>
    <string>$1</string>
    <key>BundlePath</key>
    <string>$2</string>
    <key>Comment</key>
    <string>$3</string>
    <key>Enabled</key>
    <${4}/>
    <key>ExecutablePath</key>
    <string>$5</string>
    <key>MaxKernel</key>
    <string>$6</string>
    <key>MinKernel</key>
    <string>$7</string>
    <key>PlistPath</key>
    <string>$8</string>
  </dict>"
}

build_kext_patches() {
  # Build '$.Kernel.Add' entries for all kexts/plugins
  cfg 'include.kexts | keys | .[]' | while read -r key; do
    if [[ -z "$key" && ! -d "$KEXTS_DIR/$key.kext" ]]; then continue; fi

    kext="${key%/*}"; pkg="$KEXTS_DIR/$kext.kext/Contents"
    # Resolve plugin kext name and pkg path
    if [[ $key != "$kext" ]]; then
      kext="${key##*/}"; pkg="$(find "$pkg" -name "${kext}.kext")/Contents"
    fi

    # Build Kext entry values
    Arch=$(cfg "include.kexts.\"$key\".Arch")                     #A
    BundlePath=$(cfg "include.kexts.\"$key\".BundlePath")         #B
    Comment=$(cfg "include.kexts.\"$key\".Comment")               #C
    Enabled=$(cfg "include.kexts.\"$key\".Enabled")               #D
    ExecutablePath=$(cfg "include.kexts.\"$key\".ExecutablePath") #E
    MaxKernel=$(cfg "include.kexts.\"$key\".MaxKernel")           #F
    MinKernel=$(cfg "include.kexts.\"$key\".MinKernel")           #G
    PlistPath=$(cfg "include.kexts.\"$key\".PlistPath")           #H

    # Default Kext entry values (placeholders)
    A='Any'
    B=$(sed -r "s|^$KEXTS_DIR/||" <<< "${pkg%/Contents*}")
    C="$key"
    D=$([[ -z $(cfg "exclude.kexts.$key") ]] && echo "true" || echo "false")
    E=$(find "$pkg/MacOS" -mindepth 1 2>/dev/null \
      | sed -r "s|^${pkg%/Contents*}/||")
    F=""
    G=""
    H=$(find "$pkg" -maxdepth 1 -name "Info.plist" 2>/dev/null\
      | sed -r "s|^${pkg%/Contents*}/||")

    # Append Kext entry
    offset=$(($(wc -l <<< "$KERNEL_ADD")-1))
    entry=$(awk '{printf "%s\\n", $0}'\
      <<< "$(KEXT_ADD_ENTRY "${Arch:-$A}" "${BundlePath:-$B}" "${Comment:-$C}" "${Enabled:-$D}" "${ExecutablePath:-$E}" "${MaxKernel:-$F}" "${MinKernel:-$G}" "${PlistPath:-$H}")")
    KERNEL_ADD=$(sed "${offset}s|$|\\n${entry}|" <<< "$KERNEL_ADD" | grep -Ev "^$")

    # Create plist patch
    echo "$KERNEL_ADD" > "$BUILD_DIR"/.patches/KERNEL_ADD.plist
  done
  
  KERNEL_ADD="$(cat "$BUILD_DIR"/.patches/KERNEL_ADD.plist 2>/dev/null)"
}

################################################################################
#                                 Tool Patches                                 #
################################################################################

TOOLS_ADD=$'<array>\n</array>'
TOOL_ADD_ENTRY() {
  echo \
"  <dict>
    <key>Arguments</key>
    <string>$1</string>
    <key>Auxiliary</key>
    <${2}/>
    <key>Comment</key>
    <string>$3</string>
    <key>Enabled</key>
    <${4}/>
    <key>Flavour</key>
    <string>$5</string>
    <key>FullNvramAccess</key>
    <${6}/>
    <key>Name</key>
    <string>$7</string>
    <key>Path</key>
    <string>$8</string>
    <key>RealPath</key>
    <${9}/>
    <key>TextMode</key>
    <${10}/>
  </dict>"
}

build_tool_patches() {
  # Build '$.Misc.Tools' entries for all tools
  cfg 'include.tools[]' | while read -r key; do
    # if [[ -z "$key" && ! -d "$KEXTS_DIR/$key.kext" ]]; then continue; fi

    # Build Tool entry values
    Arguments=''
    Auxiliary='true'
    Comment="$key"
    Enabled=$([[ -z $(cfg "exclude.tools.$key") ]] && echo "true" || echo "false")
    Flavour='Auto'
    FullNvramAccess='false'
    Name="$key.efi"
    Path="$key.efi"
    RealPath='false'
    TextMode='false'

    # Append Tool entry
    offset=$(($(wc -l <<< "$TOOLS_ADD")-1))
    entry=$(awk '{printf "%s\\n", $0}'\
      <<< "$(TOOL_ADD_ENTRY "$Arguments" "$Auxiliary" "$Comment" "$Enabled" "$Flavour" "$FullNvramAccess" "$Name" "$Path" "$RealPath" "$TextMode")")
    TOOLS_ADD=$(sed "${offset}s|$|\\n${entry}|" <<< "$TOOLS_ADD" | grep -Ev "^$")
    
    # Create plist patch
    echo "$TOOLS_ADD" > "$BUILD_DIR"/.patches/TOOLS_ADD.plist
  done

  TOOLS_ADD="$(cat "$BUILD_DIR"/.patches/TOOLS_ADD.plist 2>/dev/null)"
}