## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
""""""

from os import getcwd

from typing import Tuple, Union, Optional, Iterator

from ocebuild.parsers.dict import nested_get, nested_set
from ocebuild.parsers.specifier import parse_specifier
from ocebuild.parsers.yaml import parse_yaml
from ocebuild.pipeline.build import _iterate_entries
from ocebuild.sources.resolver import *


def _category_extension(category: str) -> Tuple[str, str]:
  """Determine the file extension for the category."""
  if   category == 'ACPI':
    ext = '.aml';   kind = 'SSDT'
  elif category == 'Kexts':
    ext = '.kext';  kind = 'Kext'
  else:
    ext = '.efi';   kind = 'Binary'
  return ext, kind

def _format_resolver(resolver: Union[GitHubResolver, DortaniaResolver, PathResolver, None],
                     as_specifier: bool=False) -> str:
  """"""
  resolution: str = ''

  # Add the resolver or specifier name
  if isinstance(resolver, GitHubResolver):
    resolution += f'{resolver.repository}@github'
  elif isinstance(resolver, DortaniaResolver):
    resolution += f'acidanthera/{resolver.__name__}@github'
  elif isinstance(resolver, PathResolver):
    resolution += f'{resolver.__name__}@file'
  else:
    return '*' if as_specifier else None

  # Add the resolver or specifier version/commit
  resolver_props = dict(resolver)
  if   'commit' in resolver_props:
    resolution += f"#commit={resolver_props['commit']}"
  elif as_specifier and 'tag' in resolver_props:
    resolution += f":{resolver_props['tag']}"
  elif 'version' in resolver_props:
    resolution += f":{resolver_props['version']}"
  elif isinstance(resolver, DortaniaResolver):
    resolution += f":{resolver.__specifier__}"
  elif isinstance(resolver, PathResolver):
    resolution += f":{resolver.path}"
  
  return resolution

def read_lockfile(lockfile_path: str) -> dict:
  lockfile = {}
  with open(lockfile_path, 'r', encoding='UTF-8') as f:
    lockfile, metadata = parse_yaml(f, frontmatter=True)
  return lockfile

def resolve_specifiers(build_config: dict,
                       lockfile: dict,
                       base_path: str=getcwd(),
                       update: bool=False,
                       force: bool=False,
                       *args,
                       __wrapper: Optional[Iterator]=None,
                       **kwargs
                       ) -> dict:
  """"""
  resolvers = {}
  default_build = nested_get(build_config, ['OpenCorePkg', 'OpenCore', 'build'])
  # Handle interactive mode for iterator
  iterator = _iterate_entries(build_config)
  if __wrapper is not None: iterator = __wrapper(iterator)
  # Resolve the specifiers for each entry in the build configuration
  for category, name, entry in iterator:
    # Prune matching resolvers and remove outdated entries from lockfile
    resolver = parse_specifier(name, entry, base_path=base_path)
    specifier = _format_resolver(resolver, as_specifier=True)
    if   force or update: pass #de-op
    elif specifier in lockfile: continue

    # Resolve the specifier
    resolver_props = dict(__category=category, __resolver=resolver)
    try:
      if resolver is None:
        nested_set(build_config, [category, name, 'specifier'], '*')
      elif isinstance(resolver, PathResolver):
        # Resolve the path for the specifier
        path = resolver.resolve(strict=True)
        resolver_props['path'] = path
      elif isinstance(resolver, (GitHubResolver, DortaniaResolver)):
        # Extract the build type (default to OpenCore build type)
        build = nested_get(entry, ['build'], default=default_build)
        resolver_props['build'] = build

        # Resolve the URL for the specifier
        url = resolver.resolve(build=build)
        resolver_props['url'] = url

        # Extract the version or commit from the resolver
        if   'version' in (props := dict(resolver)):
          resolver_props['version'] = props['version']
        # elif 'commit' in props:
        #   resolver_props['commit'] = props['commit']
      else:
        raise ValueError(f'Invalid resolver: {resolver}')
      
      # Format the resolution
      resolver_props['resolution'] = _format_resolver(resolver)
      resolver_props['specifier'] = specifier
    except ValueError:
      continue #TODO: Add warning
    except FileNotFoundError:
      continue #TODO: Add warning
    else:
      # Check if the resolution is already in the lockfile
      if   force: pass
      elif update and specifier in lockfile:
        lockfile_entry = lockfile[specifier]
        if 'resolution' in resolver_props:
          if resolver_props['resolution'] == lockfile_entry['resolution']:
            continue

      # Extract additional properties from the entry
      ext, kind = _category_extension(category)
      resolver_props['__filepath'] = nested_get(entry, ['__filepath'],
                                                default=f'EFI/OC/{category}/{name}{ext}')
      resolver_props['kind'] = nested_get(entry, ['__kind'], default=kind)

      # Add the resolver to the list of resolvers
      resolvers[name] = resolver_props

  return resolvers


__all__ = [
  # Functions (2)
  "read_lockfile",
  "resolve_specifiers"
]
