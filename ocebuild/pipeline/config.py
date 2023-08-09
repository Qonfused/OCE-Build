## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Methods for retrieving and handling config.plist files and patches."""

from functools import partial

from typing import Dict, List, Optional, Tuple, Union

from ocebuild.filesystem import glob
from ocebuild.parsers.dict import *
from ocebuild.parsers.plist import parse_plist
from ocebuild.parsers.schema import parse_schema
from ocebuild.parsers.yaml import parse_yaml
from ocebuild.pipeline.kexts import extract_kexts, sort_kext_cfbundle
from ocebuild.pipeline.ssdts import extract_ssdts, sort_ssdt_symbols
from ocebuild.sources import request
from ocebuild.sources.github import github_file_url

from third_party.cpython.pathlib import Path


ENTRIES_MAP = {
  'ACPI': ('ACPI', 'Add'),
  'Drivers': ('UEFI', 'Drivers'),
  'Kexts': ('Kernel', 'Add'),
  'Tools': ('Misc', 'Tools'),
}
"""A mapping of config.plist build entry types to their respective paths."""

def read_config(filepath: str,
                frontmatter: bool=False,
                flags: Optional[List[str]]=None
                ) -> Tuple[dict, Union[dict, None]]:
  """Reads a configuration file.

  Args:
    filepath: The path to the configuration file.
    frontmatter: Whether to include the file's frontmatter.
    flags: The flags to apply to the configuration file.

  Raises:
    ValueError: If the file extension is not supported.

  Returns:
    The configuration file.

    If `frontmatter` is `True`, a tuple containing:
      - The configuration file.
      - The frontmatter of the configuration file.
  """
  if not flags: flags = []
  with open(filepath, 'r', encoding='UTF-8') as f:
    file_name = Path(filepath).name
    file_ext = Path(filepath).suffix
    if   file_ext in ('.plist',):
      file = parse_plist(f)
      if frontmatter:
        return file, None
    elif file_ext in ('.yml', '.yaml'):
      if frontmatter:
        file, frontmatter = parse_yaml(f, flags=flags, frontmatter=True)
        return file, frontmatter
      else:
        file = parse_yaml(f, flags=flags)
    elif file_name in ('.serialdata',):
      serialdata, frontmatter = parse_yaml(f, flags=flags, frontmatter=True)
      file = { 'PlatformInfo': { 'Generic': serialdata } }
      return file, frontmatter
    else:
      raise ValueError(f"Unsupported file extension: {file_ext}")

  return file

def apply_preprocessor_tags(a: dict,
                            b: dict,
                            tags: List[Tuple[str, List[str], Union[str, None]]]
                            ) -> None:
  """Applies preprocessor tags from dict `b` on dict `a`.

  Args:
    a: The dict to apply preprocessor tags to.
    b: The dict annotated by the preprocessor tags.
    tags: The preprocessor tags to apply.

  Raises:
    ValueError: If the tag is not recognized.

  Notes:
    Preprocessor tags are applied in the following order:
    - @append: Append values from `b` to `a`.
    - @delete: Delete `a` and `b` if `b` is empty.
    - @fallback: Use `b` if `a` is empty.
    - @override: Override `a` with `b` if `a` contains the same key.
    - @prepend: Prepend values from `b` to `a`.
  """
  for tag, tree, options in tags:
    # Get values for a and b at the given path
    v_a, v_b = nested_get(a, tree), nested_get(b, tree)
    filtered = list(filter(lambda x: x is not None, [v_a, v_b]))
    # Handle preprocessor tags
    if   tag == '@append':
      if options is None: nested_set(a, tree, v_a + v_b)
      else:
        entry = options.join(map(str, filtered))
        nested_set(a, tree, entry)
    elif tag == '@delete':
      def del_key(keys):
        try: nested_del(a, keys)
        except KeyError: pass
      if options is not None:
        for key in options.split(','):
          del_key(keys=key.split('.'))
        # Skip cleanup
        continue
      elif v_b is None:
        del_key(keys=tree)
    elif tag == '@fallback':
      nested_set(a, tree, v_b if not v_a else v_a)
    elif tag == '@override':
      # Handle overrides for object arrays (match on primary key)
      if (primary_key := options) and isinstance(tree[-1], int):
        # Tag is on a key in the object array that may not be the primary key
        if isinstance(parent_dict := nested_get(b, tree), dict):
          # Find index of object in parent array to override
          for idx, entry in enumerate(nested_get(a, tree[:-1])):
            if entry[primary_key] == parent_dict[primary_key]:
              # Override object in parent array with new object
              nested_set(a, tree[:-1] + [idx], merge_dict(entry, parent_dict))
              break
          # Cleanup parent entry
          nested_del(b, tree)
          continue
      # Handle overrides for dictionaries
      else: nested_set(a, tree, v_b)
    elif tag == '@prepend':
      if options is None: nested_set(a, tree, v_b + v_a)
      else:
        entry = options.join(map(str, reversed(filtered)))
        nested_set(a, tree, entry)
    else:
      raise NotImplementedError(f"Unrecognized preprocessor tag: {tag}")
    # Cleanup dict b by deleting the (now duplicate) entry
    try: nested_del(b, tree)
    except KeyError: pass

def merge_configs(base: Union[str, Path],
                  *patches: Union[str, Path],
                  flags: Optional[List[str]]=None
                  ) -> Dict:
  """Merges a set of plist or yaml config files into a single config.

  Args:
    base: The base config file.
    *patches: The patch config files.
    flags: The flags to apply to the configuration file.

  Returns:
    The merged config.

  Raises:
    ValueError: If a patch file is not a plist or yaml file.

  Example:
    >>> merge_configs('base.plist', 'patch1.yml', 'patch2.plist', 'patch2.yaml')
    {...}
  """
  base_config = read_config(base)
  if not flags: flags = []

  # Parse config patches
  for filepath in patches:
    patch, frontmatter = read_config(filepath, flags=flags, frontmatter=True)
    if isinstance(frontmatter, dict):
      flags += nested_get(frontmatter, ['flags'], default=[])
      if tags := nested_get(frontmatter, ['tags']):
        apply_preprocessor_tags(base_config, patch, tags)
      base_config = merge_dict(base_config, patch)

  return base_config

def get_configuration_schema(repository: str='acidanthera/OpenCorePkg',
                             branch: str = 'master',
                             tag: Union[str, None] = None,
                             commit: Union[str, None] = None,
                             get_sample: bool=False,
                             **kwargs
                             ) -> Union[dict, Tuple[dict, dict]]:
  """Reads the Sample.plist schema from a OpenCorePkg version."""

  # Resolve file urls for the given repository parameters.
  file_url = partial(github_file_url,
                     repository=repository,
                     branch=branch,
                     tag=tag,
                     commit=commit,
                     raw=True)

  # Get the reference configuration and sample plist urls
  configuration_url = file_url(path='Docs/Configuration.tex')
  sample_plist_url = file_url(path='Docs/Sample.plist')

  sample_plist = parse_plist(request(url=sample_plist_url).text())
  with request(url=configuration_url).text() as file:
    schema = parse_schema(file, sample_plist, **kwargs)

  if get_sample: return schema, sample_plist

  return schema

def apply_schema_defaults(config: dict, schema: dict, sample: dict=None) -> dict:
  """Applies a configuration schema to a configuration file."""

  for flat_tree, value in flatten_dict(schema).items():
    tree = parse_tree(flat_tree)
    ptree = tree[:-1]
    key = tree[-1]

    # Remove parent entries that are not in the sample plist
    if nested_get(sample, ptree) is None:
      try:
        nested_del(schema, ptree)
      except KeyError: pass
      continue

    # Apply default values against all object array entries
    if isinstance(ptree[-1], int):
      parent_entry = nested_get(config, ptree[:-1])
      for i, entry in enumerate(parent_entry):
        if entry.get(key) is None:
          nested_get(config, ptree[:-1])[i][key] = value
    # Apply default values against all object entries
    else:
      parent_entry = nested_get(config, ptree)
      if parent_entry.get(key) is None:
        nested_set(config, tree, value)

  return config

#TODO: Sort kexts by dependency order, including support for:
# - Including existing entry properties (pointing to an existing `BundlePath`)
# - Disable entries on:
#   - Duplicate CFBundleIdentifiers with overlapping Max/MinKernel ranges
#   - Missing CFBundleIdentifiers (i.e. unresolved dependencies)
#   - Missing CFBundleIdentifiers/CFBundleExecutable fields in Info.plist

def acpi_entries(acpi_dir: Union[str, Path]) -> List[dict]:
  """Returns a list of ACPI entries for the given ACPI directory."""
  ssdts = extract_ssdts(acpi_dir, persist=True)
  sources = list(map(lambda e: e['source'], ssdts.values()))
  sorted_ssdts = sort_ssdt_symbols(sources)

  entries = []
  for ssdt in sorted_ssdts:
    if not ssdt in ssdts: continue
    entry = {
      'Enabled': True,
      'Path': ssdts[ssdt]['__path'].replace('./', '')
    }
    entries.append(entry)

  return entries

def drivers_entries(drivers_dir: Union[str, Path]) -> List[dict]:
  """Returns a list of driver entries for the given drivers directory."""
  drivers = glob(drivers_dir, pattern='**/*.efi')

  entries = []
  for driver in drivers:
    entry = {
      'Enabled': True,
      'Path': driver.as_posix().replace(Path(drivers_dir).as_posix() + '/', '')
    }
    entries.append(entry)

  return entries

def kexts_entries(kext_dir: Union[str, Path]) -> List[dict]:
  """Returns a list of kext entries for the given kext directory."""
  kexts = extract_kexts(kext_dir)
  sources = list(map(lambda e: e['__extracted'], kexts.values()))
  sorted_kexts = sort_kext_cfbundle(sources)

  def fmt_relative(p: Path):
    path = Path(p).as_posix()
    parent = Path(kext_dir).as_posix()
    return path.replace(parent + '/', '')

  entries = []
  for kext in sorted_kexts:
    path = Path(kext_dir, kext['__path'])

    bundle_path = fmt_relative(path)
    plist_path = fmt_relative(glob(path, '**/Info.plist', first=True))
    entry = {
      'BundlePath': bundle_path,
      'Enabled': True,
      'PlistPath': plist_path.replace(bundle_path + '/', ''),
    }

    if executable_path := glob(path, f"**/{kext['executable']}", first=True):
      executable_path = fmt_relative(executable_path)
      entry['ExecutablePath'] = executable_path.replace(bundle_path + '/', '')

    entries.append(entry)

  return entries

def tools_entries(tools_dir: Union[str, Path]) -> List[dict]:
  """Returns a list of tool entries for the given tools directory."""
  tools = glob(tools_dir, pattern='**/*.efi')

  entries = []
  for tool in tools:
    entry = {
      'Enabled': True,
      'Name': tool.stem,
      'Path': tool.as_posix().replace(Path(tools_dir).as_posix() + '/', '')
    }
    entries.append(entry)

  return entries

def update_entries(config_path: Union[str, Path],
                   build_config: Optional[dict]=None,
                   clean: bool=False
                   ) -> dict:
  """Updates the build entries of an OpenCore configuration file.

  This function scans the `ACPI`, `Drivers`, `Kexts`, and `Tools` folders
  relative to the configuration file and updates their corresponding entries.

  Args:
    config_path: The path to the OpenCore configuration file.
    clean: Whether to override existing entries from the configuration file.

  Returns:
    A dictionary containing the updated configuration entries.
  """

  def oc_dir(name: str) -> Path:
    return Path(config_path, f'../{name}').resolve()

  # Generate new entries for each present build entry
  config = parse_plist(open(config_path, 'r'))
  entry_methods = {
    'ACPI':     (acpi_entries,    'Path'),
    'Drivers':  (drivers_entries, 'Path'),
    'Kexts':    (kexts_entries,   'BundlePath'),
    'Tools':    (tools_entries,   'Path')
  }
  for category, (method, primary_key) in entry_methods.items():
    entries: List[dict] = method(oc_dir(category))
    build_entries = build_config.get(category, {})

    keys = ENTRIES_MAP[category]
    if clean: nested_set(config, keys, [])
    base_entries = nested_get(config, keys)

    for idx, entry in enumerate(method(oc_dir(category))):
      # Merge new entries with build config properties
      name = Path(entry[primary_key]).stem
      if props := nested_get(build_entries, [name, 'properties']):
        entries[idx].update(props)
      # Merge new entries with existing config entries
      base = next((e for e in base_entries
                  if e[primary_key] == entry[primary_key]), {})
      for key, value in base.items():
        if key not in entry:
          entries[idx][key] = value

    # Update config with new entries
    nested_set(config, keys, entries)

  return config


__all__ = [
  # Constants (1)
  "ENTRIES_MAP",
  # Functions (10)
  "read_config",
  "apply_preprocessor_tags",
  "merge_configs",
  "get_configuration_schema",
  "apply_schema_defaults",
  "acpi_entries",
  "drivers_entries",
  "kexts_entries",
  "tools_entries",
  "update_entries"
]
