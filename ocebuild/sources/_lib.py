## @file
# Network helper functions.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

from __future__ import annotations

from io import TextIOWrapper
from json import load as json_load
from ssl import _create_unverified_context as skip_ssl_verify
from urllib.error import HTTPError
from urllib.request import urlopen, Request

from typing import Union


class RequestWrapper():
  """Wrapper for urllib.request.Request to provide a nicer interface."""

  def __init__(self, response: any):
    self._wrapped_response = response

  def __enter__(self) -> RequestWrapper:
    return self

  def __exit__(self, *args: object) -> None:
    return None

  def __getattr__(self, attr):
    return getattr(self._wrapped_response, attr)

  def json(self, *args, **kargs) -> any:
    """Return the response as JSON."""
    return json_load(self._wrapped_response, *args, **kargs)
  
  def text(self, *args, **kargs) -> TextIOWrapper:
    """Return the response as text."""
    return TextIOWrapper(self._wrapped_response, *args, **kargs)

def request(url: Union[str, Request]) -> any:
  """Simple wrapper over urlopen for skipping SSL verification."""
  try:
    return RequestWrapper(urlopen(url, context=skip_ssl_verify()))
  except HTTPError as e:
    raise e
