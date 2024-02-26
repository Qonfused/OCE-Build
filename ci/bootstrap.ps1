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

function Bootstrap-Exe {
  param (
    [string]$uri,
    [string]$dest
  )

  # Trap native errors halt script execution on any error
  $PSNativeCommandUseErrorActionPreference = $true
  $ErrorActionPreference = 'Stop'

  # Download the executable through a BITS transfer job
  $ProgressPreference = 'SilentlyContinue'
  $bitsJobObj = Start-BitsTransfer $uri `
    -Destination $dest `
    -DisplayName "Downloading $uri"

  switch ($bitsJobObj.JobState) {
    'Transferred' {
      Complete-BitsTransfer -BitsJob $bitsJobObj
      break
    }
    'Error' {
      throw 'Error downloading'
    }
  }

  # Restore the progress preference
  $ProgressPreference = 'Continue'
}

Write-Host "Downloading OCE Build CLI..."

$BINARY_URL="$OCEBUILD_URL/releases/download/$OCEBUILD_VERSION/ocebuild.exe"
$BINARY_PATH="$env:TEMP\ocebuild.exe"
Bootstrap-Exe -uri $BINARY_URL -dest $BINARY_PATH

Write-Host ""

$ARGS = $($arguments -join ' ')
Start-Process -Wait $BINARY_PATH -NoNewWindow -ArgumentList $ARGS
Remove-Item $BINARY_PATH
