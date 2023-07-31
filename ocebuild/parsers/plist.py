## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Parser for converting property list to a Python dictionary."""

from io import BufferedReader, TextIOWrapper

from typing import Union

from third_party.cpython.plistlib import dumps, loads, FMT_BINARY, FMT_XML
from third_party.cpython.plistlib import PlistFormat


PLIST_FORMATS = { 'xml': FMT_XML, 'binary': FMT_BINARY }
"""Mapping of format names to plistlib `PlistFormat` enum values."""

def parse_plist(lines: Union[str, bytes, BufferedReader, TextIOWrapper],
                fmt: Union[None, PlistFormat] = None,
                dict_type=dict
                ) -> dict:
  """Parses a native dictionary from a plist.

  Args:
    lines: Property list (plist) lines.
    fmt: Format of the plist file.
    dict_type: Type of dictionary to return.

  Returns:
    A dictionary containing the parsed plist.
  """
  if isinstance(lines, (BufferedReader, TextIOWrapper)):
    lines = lines.read()
  if isinstance(lines, str):
    lines = str.encode(lines)
  return loads(lines, fmt=fmt, dict_type=dict_type)

def write_plist(config: dict,
                fmt: PlistFormat = FMT_XML,
                sort_keys: bool=False
                ) -> str:
  """Writes a native dictionary to a plist.

  Args:
    config: Dictionary to be written.
    fmt: Format of the plist file.
    sort_keys: Whether to sort the keys in the output.

  Returns:
    A string containing the written plist.
  """
  return dumps(config, fmt=fmt, sort_keys=sort_keys).decode(encoding='UTF-8')


__all__ = [
  # Constants (1)
  "PLIST_FORMATS",
  # Functions (2)
  "parse_plist",
  "write_plist"
]
