## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Methods for retrieving and handling config.plist files and patches."""

from functools import partial

from typing import Dict, List, Optional, Tuple, Union

from ocebuild.parsers.dict import merge_dict, nested_del, nested_get, nested_set
from ocebuild.parsers.plist import parse_plist
from ocebuild.parsers.schema import parse_schema
from ocebuild.parsers.yaml import parse_yaml
from ocebuild.sources import request
from ocebuild.sources.github import github_file_url
from ocebuild.sources.resolver import PathResolver


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
    file_ext = PathResolver(filepath).suffix
    if   file_ext in ('.plist'):
      file = parse_plist(f)
      if frontmatter:
        return file, None
    elif file_ext in ('.yml', '.yaml'):
      if frontmatter:
        file, frontmatter = parse_yaml(f, flags=flags, frontmatter=True)
        return file, frontmatter
      else:
        file = parse_yaml(f, flags=flags)
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
        entry = (v_b[0], options.join([str(x[1]) for x in filtered]))
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
        entry = (v_b[0], options.join([str(x[1]) for x in reversed(filtered)]))
        nested_set(a, tree, entry)
    else:
      raise NotImplementedError(f"Unrecognized preprocessor tag: {tag}")
    # Cleanup dict b by deleting the (now duplicate) entry
    try: nested_del(b, tree)
    except KeyError: pass

def merge_configs(base: Union[str, PathResolver],
                  *patches: Union[str, PathResolver],
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
  base_config, _ = read_config(base)
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


__all__ = [
  # Functions (4)
  "read_config",
  "apply_preprocessor_tags",
  "merge_configs",
  "get_configuration_schema"
]
