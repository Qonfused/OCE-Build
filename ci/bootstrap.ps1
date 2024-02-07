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

  $ProgressPreference = 'Continue'
  Start-Process -Wait $dest -NoNewWindow -ArgumentList $args
  Remove-Item $dest
}

$BINARY_URL="$OCEBUILD_URL/releases/download/$OCEBUILD_VERSION/ocebuild.exe"
Bootstrap-Exe -uri $BINARY_URL -dest ocebuild.exe `
  $($arguments -join ' ')
