## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Methods for handling and manipulating the build configuration."""

from shutil import unpack_archive
from tempfile import mkdtemp

from typing import Dict, Iterator, List, Optional, Tuple, Union

from ocebuild.filesystem import copy, glob
from ocebuild.filesystem.archives import extract_archive
from ocebuild.filesystem.cache import UNPACK_DIR
from ocebuild.parsers.dict import nested_get, nested_set
from ocebuild.parsers.yaml import parse_yaml
from ocebuild.pipeline.lock import _category_extension

from third_party.cpython.pathlib import Path


def _set_var_default(build_vars: dict, name: str, default: str):
  """Set a variable to a default value if it is not already set."""
  if not (variable := nested_get(build_vars, ['variables', name])):
    variable = default
    nested_set(build_vars, ['variables', name], variable)
  return variable

def read_build_file(filepath: str,
                    normalize_entries: bool=True
                    ) -> Tuple[dict, dict, List[str]]:
  """Read the build configuration from the specified build file.

  Args:
    filepath: The path to the build file.
    normalize_entries: Whether to normalize the entries in the build file.

  Returns:
    A tuple containing:
      - The build configuration.
      - The build variables.
      - The build flags.
  """
  with open(filepath, 'r', encoding='UTF-8') as f:
    build_config, build_vars = parse_yaml(f, frontmatter=True)

  # Extract the OpenCore build configuration
  version = _set_var_default(build_vars, 'version', 'latest')
  build = _set_var_default(build_vars, 'build', 'RELEASE')
  target = _set_var_default(build_vars, 'target', 'X64')

  # Add additional flags from the build configuration
  flags = nested_get(build_vars, ['flags'])
  if build not in flags:  flags += [build]
  if target not in flags: flags += [target]

  # Normalize the entries in the build configuration
  if normalize_entries:
    build_config['OpenCorePkg'] = {
      'OpenCore': {
        '__filepath': 'EFI/OC/OpenCore.efi',
        'specifier': version,
        'repository': 'acidanthera/OpenCorePkg',
        'build': build
      },
      'OcBinaryData': {
        '__filepath': 'EFI/OC/.',
        'specifier': 'latest',
        'repository': 'acidanthera/OcBinaryData',
        'branch': 'master',
        'build': build,
        'tarball': True
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

def unpack_build_entries(resolvers: List[dict],
                         project_dir: Path,
                         *args,
                         __wrapper: Optional[Iterator]=None,
                         **kwargs) -> dict:
  """Unpacks the build entries from the build configuration."""

  # Handle interactive mode for iterator
  iterator = resolvers
  if __wrapper is not None: iterator = __wrapper(iterator, *args, **kwargs)

  extracted = {}
  for entry in iterator:
    tmpdir: Path
    # Handle extracting remote entries
    if (url := entry.get('url')):
      with extract_archive(url, persist=True) as tmpdir:
        for archive in tmpdir.glob('**/*.zip'):
          unpack_archive(archive, tmpdir.joinpath(archive.name))
    # Handle extracting local entries
    elif (path := entry.get('path')):
      tmpdir = Path(mkdtemp(dir=UNPACK_DIR))
      src = project_dir.joinpath(path)
      copy(src, tmpdir.joinpath(tmpdir, src.name))
    # Skip wildcard specifiers
    elif entry.get('specifier') == '*': continue
    # Update extracted paths
    entry['__extracted'] = tmpdir
    nested_set(extracted, [entry['__category'], entry['name']], tmpdir)

  return extracted

def validate_build_directory(build_config: dict,
                             out_dir: Union[str, Path]
                             ) -> Dict[str, List[str]]:
  """Verifies that all build entries are present in the build directory."""

  missing_entries = {}
  oc_dir = glob(out_dir, '**/OC/OpenCore.efi', first=True).parent
  for category, entries in build_config.items():
    path = oc_dir.joinpath(category)
    if not path.exists(): continue
    ext, _ = _category_extension(category)
    matched_entries = set(f.stem for f in glob(path, f'**/*{ext}'))
    for name, entry in entries.items():
      if name not in matched_entries:
        missing_entries.setdefault(category, []).append(name)
      for bundled in entry.get('bundled', []):
        if bundled not in matched_entries:
          missing_entries.setdefault(category, []).append(bundled)

  return missing_entries


__all__ = [
  # Functions (3)
  "read_build_file",
  "unpack_build_entries",
  "validate_build_directory"
]
