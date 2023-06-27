## @file
# Stacktrace introspection methods used for testing and at runtime.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

import sys
from contextlib import contextmanager


@contextmanager
def disable_exception_traceback(tracebacklimit: int=0):
  """Suppresses stack trace information from an exception."""
  default_value = sys.__dict__.get('tracebacklimit', 1000)
  sys.tracebacklimit = tracebacklimit
  yield
  sys.tracebacklimit = default_value
