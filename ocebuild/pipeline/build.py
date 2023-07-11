## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
""""""

from itertools import chain

from typing import List, Tuple

from ocebuild.parsers.dict import nested_get, nested_set
from ocebuild.parsers.yaml import parse_yaml


def __set_var_default(build_vars: dict, name: str, default: str):
  if not (variable := nested_get(build_vars, ['variables', name])):
    variable = default
    nested_set(build_vars, ['variables', name], variable)
  return variable

def _iterate_entries(build_config: dict) -> List[Tuple[str, str, dict]]:
  """Iterate over the entries in the build configuration."""
  def group_entries(category: str, entries: dict):
    return [(category, name, entry) for name, entry in entries.items()]
  return list(chain(*[group_entries(c,d) for c,d in build_config.items()]))

def read_build_file(filepath: str,
                    normalize_entries: bool=True
                    ) -> Tuple[dict, dict, List[str]]:
  """Read the build configuration from the specified build file."""
  with open(filepath, 'r', encoding='UTF-8') as f:
    build_config, build_vars = parse_yaml(f, frontmatter=True)
  
  # Extract the OpenCore build configuration
  version = __set_var_default(build_vars, 'version', 'latest')
  build = __set_var_default(build_vars, 'build', 'RELEASE')
  target = __set_var_default(build_vars, 'target', 'X64')

  # Add additional flags from the build configuration
  flags = nested_get(build_vars, ['flags'])
  if not build in flags:  flags += [build]
  if not target in flags: flags += [target]

  # Normalize the entries in the build configuration
  if normalize_entries:
    build_config['OpenCorePkg'] = {
      'OpenCore': {
        '__filepath': 'EFI/OC/OpenCore.efi',
        'specifier': version,
        'repository': 'acidanthera/OpenCorePkg',
        'build': build
      }
    }
    for category, entries in build_config.items():
      # Reconstruct an equivalent dictionary entry
      if isinstance(entries, list):
        build_config[category] = {}
        entries = { k: '*' for k in entries }
      # Normalize the specifier for each entry
      if isinstance(entries, dict):
        for name, entry in entries.items():
          # Handle string specifiers
          if not isinstance(entry, dict):
            build_config[category][name] = {}
            nested_set(build_config, [category, name, 'specifier'], entry)

  return build_config, build_vars, flags


__all__ = [
  # Functions (1)
  "read_build_file"
]
