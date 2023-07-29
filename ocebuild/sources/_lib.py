## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Network helper functions."""

from __future__ import annotations

from io import TextIOWrapper
from json import load as json_load
from ssl import _create_unverified_context as skip_ssl_verify
from urllib.error import HTTPError
from urllib.request import Request, urlopen

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

def request(url: Union[str, Request], *args, **kwargs) -> any:
  """Simple wrapper over urlopen for skipping SSL verification.

  Args:
    url: The url to open.
    *args: Additional arguments to pass to urlopen.
    **kwargs: Additional keyword arguments to pass to urlopen.

  Raises:
    HTTPError: If the url could not be retrieved.

  Returns:
    The response from urlopen wrapped in a RequestWrapper class.
  """
  try:
    #pylint: disable=consider-using-with
    response = urlopen(url, context=skip_ssl_verify(), *args, **kwargs)
    return RequestWrapper(response)
  except HTTPError as e:
    print(f'Could not retrieve url: {e.url}')
    raise e

__all__ = [
  # Functions (1)
  "request",
  # Classes (1)
  "RequestWrapper"
]
