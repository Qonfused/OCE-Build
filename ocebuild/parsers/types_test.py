## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

import pytest

from .types import *

def test_encode_data():
  # Test hexadecimal encoding for multiple input formats
  assert encode_data('<01 00 00 00>') == b'\x01\x00\x00\x00'
  assert encode_data('01000000')      == b'\x01\x00\x00\x00'
  assert encode_data('AQAAAA==')      == b'\x01\x00\x00\x00'
  # Test default cases
  assert encode_data('<>')  == b''
  assert encode_data('')    == b''
  with pytest.raises(ValueError):
    assert encode_data('==') # Reject invalid base64 encoding
