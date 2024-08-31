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

$OCEBUILD_URL="https://github.com/Qonfused/OCE-Build"
$OCEBUILD_VERSION="nightly"

function Bootstrap {
  param (
    [string]$uri,
    [string]$dest
  )

  # Trap native errors halt script execution on any error
  $PSNativeCommandUseErrorActionPreference = $true
  $ErrorActionPreference = 'Stop'

  # Download the executable from the specified URI
  Invoke-WebRequest -Uri $uri -OutFile $dest

  # Grant read execute permissions to the destination file
  if ($IsWindows) {
    icals $dest /remove 'Everyone'
    icals $dest /grant  'Everyone:(RX)'
  } else {
    chmod +x $dest.replace('/\', '/')
  }
}

Write-Host "Downloading OCE Build CLI..."

# Check the OS platform to determine the executable file extension
$EXT = if ($IsWindows) { ".exe" } elseif ($IsLinux) { ".linux" } else { "" }

$BINARY_URL="$OCEBUILD_URL/releases/download/$OCEBUILD_VERSION/ocebuild$EXT"
$BINARY_PATH="$([System.IO.Path]::GetTempPath())\ocebuild$EXT"
Bootstrap -uri $BINARY_URL -dest $BINARY_PATH

Write-Host ""

Start-Process -Wait $BINARY_PATH -NoNewWindow -ArgumentList "build -c $pwd $patches"
Remove-Item $BINARY_PATH
