#pragma preserve-exports

## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Overrides the `plistlib` module to support backports and custom subclasses."""

import plistlib
from plistlib import InvalidFileException, FMT_BINARY, FMT_XML
from plistlib import dump, dumps, load, loads
from plistlib import PlistFormat, _FORMATS

from binascii import b2a_base64

from .. import inject_module_namespace


class UID(plistlib.UID):
  """A `plistlib.UID` subclass that enforces a 32-bit limit on the UID value.

  Apple handles UIDs assuming 32-bit unsigned integers:
    - [CF/CFBinaryPList.c#L138-L146](https://github.com/apple-oss-distributions/CF/blob/dc54c6bb1c1e5e0b9486c1d26dd5bef110b20bf3/CFBinaryPList.c#L138-L146)
    - [CF/CFPropertyList.c#L1538-L1547](https://github.com/apple-oss-distributions/CF/blob/dc54c6bb1c1e5e0b9486c1d26dd5bef110b20bf3/CFPropertyList.c#L1538-L1547)

  The original `plistlib.UID` class does not enforce this limit, so we must
  override the constructor to ensure the value is within the 32-bit limit.
  """

  def __init__(self, data):
    # Ensure MRO is cooperative with subclassing
    super(UID, self).__init__(data)

    # Hook into the `plistlib.UID` constructor
    super(plistlib.UID, self).__init__()

    # Enforce a 32-bit limit to the UID value
    if data >= 1 << 32:
      raise ValueError("UIDs cannot be >= 2**32")

#TODO: Implement _BinaryPlistWriter fixes

class _PlistWriter(plistlib._PlistWriter):

  def write_bytes(self, data):
    """Writes a base64-encoded data element to a plist file."""

    # Calculate the maximum line length (from the original _PlistWriter writer)
    indent = self.indent.replace(b"\t", b" " * 8)
    maxlinelength = max(16, 76 - len(indent * (self._indent_level - 1)))

    # Calculate the number of newlines required (from _encode_base64 binning)
    maxbinsize = (maxlinelength//4)*3
    num_newlines = len(data) / maxbinsize

    # Write the data as a single-line base64 string if no newlines are needed
    if num_newlines < 1:
      base64_data = b2a_base64(data, newline=False)
      self.simple_element("data", base64_data.decode('utf-8'))
    # Otherwise write the data as a multi-line base64 string
    else:
      super().write_bytes(data)

# Override the `plistlib` module's writer class
_FORMATS[FMT_XML]['writer'] = _PlistWriter


# Inject the `plistlib` namespace into the current module
inject_module_namespace(plistlib, namespace=globals())

__all__ = [
  "InvalidFileException",
  "FMT_XML",
  "FMT_BINARY",
  "load",
  "dump",
  "loads",
  "dumps",
  "UID"
]
