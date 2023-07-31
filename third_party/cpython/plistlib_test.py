## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

import pytest

from .plistlib import dumps, UID


def test_UID():
  instance = UID((1 << 32) - 1)
  assert instance.data == 4294967295

  with pytest.raises(ValueError):
    UID((1 << 32) + 8)

  with pytest.raises(ValueError):
    UID(1 << 64)

def test_plist_writer():

  # Ensure the `plistlib._PlistWriter` bytes method is patched
  assert dumps({ 'foo': b'\01\00' * 28 }).split(b'\n') == \
    [
      b'<?xml version="1.0" encoding="UTF-8"?>',
      b'<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">',
      b'<plist version="1.0">',
      b'<dict>',
      b'\t<key>foo</key>',
      b'\t<data>AQABAAEAAQABAAEAAQABAAEAAQABAAEAAQABAAEAAQABAAEAAQABAAEAAQABAAEAAQABAAEAAQA=</data>',
      b'</dict>',
      b'</plist>',
      b''
    ]

  assert dumps({ 'foo': b'\01\00' * 29 }).split(b'\n') == \
    [
      b'<?xml version="1.0" encoding="UTF-8"?>',
      b'<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">',
      b'<plist version="1.0">',
      b'<dict>',
      b'\t<key>foo</key>',
      b'\t<data>',
      b'\tAQABAAEAAQABAAEAAQABAAEAAQABAAEAAQABAAEAAQABAAEAAQABAAEAAQABAAEAAQAB',
      b'\tAAEAAQABAA==',
      b'\t</data>',
      b'</dict>',
      b'</plist>',
      b''
    ]
