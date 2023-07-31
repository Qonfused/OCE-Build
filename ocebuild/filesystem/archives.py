## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Methods for handling and extracting archive formats."""

from contextlib import contextmanager
from shutil import rmtree, unpack_archive
from tempfile import mkdtemp, NamedTemporaryFile
from urllib.request import Request

from typing import Generator, Union

from .cache import UNPACK_DIR

from ocebuild.parsers.regex import re_match
from ocebuild.sources import request

from third_party.cpython.pathlib import Path


@contextmanager
def extract_archive(url: Union[str, Request],
                    persist: bool=False
                    ) -> Generator[Path, str, None]:
  """Extracts a file from a URL and yields a temporary extraction directory.

  Args:
    url: URL of the archive file.
    persist: Flag to disable cleanup of the temporary directory.

  Yields:
    tmp_dir (str): Path to the temporary directory.

  Example:
    >>> with extract_archive('https://example.com/foo.zip') as tmp_dir:
    print(tmp_dir)
    # -> "/tmp/xxxxxx"
  """
  tmp_dir = mkdtemp(dir=UNPACK_DIR)
  try:
    #TODO: If github file url, test `raw.githubusercontent` redirect,
    #      otherwise parse and extract from an archive url.
    with request(url) as response:
      # Extract filename from request headers.
      filename = re_match(pattern=r'^attachment; filename="?(.*)"?;?$',
                          string=response.headers.get('Content-Disposition'),
                          group=1)
      if filename:
        extension = "".join(Path(filename).suffixes)
      elif '.' in url:
        extension = f'.{url.split(".")[-1]}'
      else:
        extension = url.rsplit("/", maxsplit=1)[-1]
      # Write archive to a temporary file.
      with NamedTemporaryFile(suffix=f'-{filename or extension}',
                              dir=UNPACK_DIR) as tmp_file:
        tmp_file.write(response.read())
        tmp_file.seek(0)
        # Extract the zip file to the temporary directory.
        unpack_archive(tmp_file.name, tmp_dir)
    # Yield the temporary directory.
    yield Path(tmp_dir)
  finally:
    # Cleanup after context exits
    if not persist: rmtree(tmp_dir)


__all__ = [
  # Functions (1)
  "extract_archive"
]
