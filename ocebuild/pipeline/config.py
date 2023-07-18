## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Methods for retrieving and handling config.plist files and patches."""

from typing import Dict, List, Tuple, Union

from ocebuild.parsers.dict import merge_dict, nested_del, nested_get, nested_set
from ocebuild.parsers.plist import parse_plist
from ocebuild.parsers.yaml import parse_yaml
from ocebuild.sources.resolver import PathResolver


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
                  *patches: Union[str, PathResolver]
                  ) -> Dict:
  """Merges a set of plist or yaml config files into a single config.

  Args:
    base: The base config file.
    *patches: The patch config files.

  Returns:
    The merged config.

  Raises:
    ValueError: If a patch file is not a plist or yaml file.

  Example:
    >>> merge_configs('base.plist', 'patch1.yml', 'patch2.plist', 'patch2.yaml')
    {...}
  """
  base_config, _ = read_config(base)

  # Parse config patches
  for filepath in patches:
    patch, frontmatter = read_config(filepath)
    if isinstance(frontmatter, dict) and 'tags' in frontmatter:
      apply_preprocessor_tags(base_config, patch, frontmatter['tags'])
    base_config = merge_dict(base_config, patch)

  return base_config

def read_config(filepath: str) -> Tuple[Dict, Union[Dict, None]]:
  """Reads a configuration file.
  
  Args:
    filepath: The path to the configuration file.

  Raises:
    ValueError: If the file extension is not supported.
  
  Returns:
    A tuple containing:
      - The configuration file.
      - The frontmatter of the configuration file.
  """
  with open(filepath, 'r', encoding='UTF-8') as f:
    file_ext = PathResolver(filepath).suffix
    if   file_ext in ('.plist'):
      file, frontmatter = parse_plist(f), None
    elif file_ext in ('.yml', '.yaml'):
      file, frontmatter = parse_yaml(f, frontmatter=True)
    else:
      raise ValueError(f"Unsupported file extension: {file_ext}")
  return file, frontmatter


__all__ = [
  # Functions (3)
  "apply_preprocessor_tags",
  "merge_configs",
  "read_config"
]
