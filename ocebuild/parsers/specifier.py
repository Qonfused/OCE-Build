## @file
# Custom specifier resolver classes and methods.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

from pathlib import Path

from typing import Dict, Optional, Union

from parsers.regex import re_match, re_search
from sources.resolver import GitHubResolver, PathResolver


def parse_specifier(name: str,
                    entry: Union[str, Dict[str, any]]
                    ) -> Union[GitHubResolver, Path, None]:
  """"""
  specifier = entry['specifier'] if isinstance(entry, dict) else entry
  parameters: Dict[str, str]=dict()
  resolver_props = { '__name__': name, '__specifier__': specifier }

  # Specifier points to a github repository
  repository: Optional[str]=None
  if (repository := re_match('[a-zA-Z0-9\\-]+\\/[a-zA-Z0-9\\-]+', specifier)):
    parameters['repository'] = repository
    params = ('branch', 'tag', 'workflow', 'commit')
    # (Priority: 1) Named specifier parameters
    if re_match(f'{repository}#[a-zA-Z\\-]+=', specifier):
      for k in params:
        if (prefix := re_match(f'#.*{k}=', specifier)):
          #TODO: Add separation for multiple parameters (,)
          parameters[k] = specifier[len(prefix):]
    # (Priority: 2) Unnamed specifier parameters
    elif (prefix := re_match(f'{repository}=', specifier)):
      parameters['tag'] = specifier[len(prefix):]
    elif (prefix := re_match(f'{repository}#', specifier)):
      pattern = specifier[len(prefix):]
      # Test for whether matched string is a valid hash sha
      if (sha_long := re_search(r'\b[0-9a-fA-F]{40}\b', pattern)):
        parameters['commit'] = sha_long
      elif (sha_short := re_search(r'\b[0-9a-fA-F]{7}\b', pattern)):
        parameters['commit'] = sha_short
      # Fall back to assignment as branch name
      else:
        parameters['branch'] = pattern
    # (Override) Named entry parameters
    if isinstance(entry, dict):
      for k in params:
        if k in entry: parameters[k] = entry[k]
    return GitHubResolver(**parameters, **resolver_props)

  # Specifier points to a local file
  if (filepath := Path(specifier)).exists():
    parameters['path'] = filepath
    return PathResolver(**parameters, **resolver_props)
