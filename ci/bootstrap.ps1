## @file
# Downloads and executes a binary release of the OCE Build CLI.
#
# Copyright (c) 2024, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

[CmdletBinding(PositionalBinding=$false)]
param (
  [parameter(ValueFromRemainingArguments)][string[]]$arguments
)

# Trap native errors halt script execution on any error
$PSNativeCommandUseErrorActionPreference = $true
$ErrorActionPreference = 'Stop'

# Check if the powershell version is less than 6.0
if ($PSVersionTable.PSVersion.Major -lt 6) {
  # Patch OS detection to properly identify the current platform
  # on older versions of PowerShell (non-Core distributions).
  if (-not $IsWindows) {
    $IsWindows = [System.Environment]::OSVersion.Platform -lt [System.PlatformID]::Unix
  }
  if (-not $IsLinux) {
    $IsLinux = ([System.Environment]::OSVersion.Platform -ge [System.PlatformID]::Unix) -and ([System.Environment]::OSVersion.Platform -ne [System.PlatformID]::MacOSX)
  }
  if (-not $IsMacOS) {
    $IsMacOS = [System.Environment]::OSVersion.Platform -eq [System.PlatformID]::MacOSX
  }
}

function Bootstrap {
  param (
    [string]$uri,
    [string]$dest
  )

  # Download the executable from the specified URI
  Invoke-WebRequest -Uri $uri -OutFile $dest

  # Grant read execute permissions to the destination file
  if (-not $IsWindows) {
    chmod +x $dest.replace('/\', '/')
  }
}

Write-Host "Downloading OCE Build CLI..."

$OCEBUILD_URL="https://github.com/Qonfused/OCE-Build"
$OCEBUILD_VERSION="nightly"

# Check the OS platform to determine the executable file extension
$EXT = if ($IsWindows) { ".exe" } elseif ($IsLinux) { ".linux" } else { "" }

$BINARY_URL="$OCEBUILD_URL/releases/download/$OCEBUILD_VERSION/ocebuild$EXT"
$BINARY_PATH="$([System.IO.Path]::GetTempPath())\ocebuild$EXT"
Bootstrap -uri $BINARY_URL -dest $BINARY_PATH

Write-Host ""

Start-Process -Wait $BINARY_PATH -NoNewWindow -ArgumentList $arguments
Remove-Item $BINARY_PATH
