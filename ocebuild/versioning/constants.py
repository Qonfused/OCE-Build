## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

from versioning.sources import github_archive_url, github_file_url


DORTANIA_CATALOG_URL = github_file_url('dortania/build-repo', 'config.json', branch='builds')

OPENCORE_PACKAGE_URL = github_archive_url('acidanthera/OpenCorePkg', branch='master')
OPENCORE_BINARY_DATA_URL = github_archive_url('acidanthera/OcBinaryData', branch='master')
