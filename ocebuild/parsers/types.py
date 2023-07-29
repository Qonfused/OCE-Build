## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Type parsing helper functions."""

from plistlib import _encode_base64

from binascii import a2b_base64, a2b_hex, hexlify

from ocebuild.parsers.regex import re_match, re_search


RE_VALID_BASE64 = r'^([a-zA-Z0-9+/]{4})*([a-zA-Z0-9+/]{3}=|[a-zA-Z0-9+/]{2}==)?$'
"""Regular expression to match a valid base64 string."""

RE_VALID_HEX = r'^([a-fA-F0-9]{2})*$'
"""Regular expression to match a valid hexadecimal string."""

def encode_data(value: str) -> bytes:
  """Encodes a base64 or hexadecimal string to a binary representation.

  Args:
    value: The base64 or hexadecimal string to encode.

  Raises:
    ValueError: If the string is not a valid base64 or hexadecimal string.

  Returns:
    A binary representation of the string.

  Examples:
    >>> encode_data('<01 00 00 00>')
    b'\\x01\\x00\\x00\\x00'
    >>> encode_data('01000000')
    b'\\x01\\x00\\x00\\x00'
    >>> encode_data('AQAAAA==')
    b'\\x01\\x00\\x00\\x00'
  """
  bits = "".join(map(lambda s: re_search(r'[a-zA-Z0-9+/=]+', s), value.split()))
  if not bits: return b''
  elif (hex_str := re_match(RE_VALID_HEX, bits)):
    return a2b_hex(hex_str)
  elif (base64_str := re_match(RE_VALID_BASE64, bits)):
    return a2b_base64(base64_str)
  else:
    raise ValueError(f'Invalid data format: {value}')

def decode_data(value: bytes, enc: str='base64') -> str:
  """Decodes a binary representation to a base64 string.

  Args:
    value: The binary representation to decode.
    enc: The encoding format to return. Valid values are 'base64' and 'hex'.

  Raises:
    ValueError: If the format is not a valid format.

  Returns:
    A base64 or hex string representation of the binary data.
  """
  if enc == 'base64':
    return _encode_base64(value).decode('UTF-8').strip()
  elif enc == 'hex':
    return hexlify(value).decode('UTF-8').strip().upper()
  else:
    raise ValueError(f'Unrecognized data format: {enc}')


__all__ = [
  # Constants (2)
  "RE_VALID_BASE64",
  "RE_VALID_HEX",
  # Functions (2)
  "encode_data",
  "decode_data"
]
