## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

import pytest

from .cache import *
from .cache import _iter_temp_dir


def test_get_temp_dir():
  def _tmpdirs(prefix): return _iter_temp_dir(prefix, dir_=UNPACK_DIR.parent)

  #NOTE: pytest will override cache as a unique caller
  assert UNPACK_DIR.exists()
  assert len(list(_tmpdirs(prefix="ocebuild-unpack-"))) == 1
