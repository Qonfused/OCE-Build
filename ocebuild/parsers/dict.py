## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Dictionary helper functions."""

from typing import Dict, List, Optional, Union

from .regex import re_search


def flatten_dict(dic: dict,
                 delimiter: str='.'
                 ) -> Dict[str, any]:
  """Flattens a dictionary.

  Args:
    dic: The dictionary to flatten.
    delimiter (optional): custom key delimiter.

  Returns:
    A flattened dictionary
  """
  flat_dict: dict={}
  def recurse_flatten(v: any, prefix: str='') -> None:
    if isinstance(v, dict):
      if not (entries := v.items()):
        flat_dict[prefix[1:]] = v
      else:
        for k, v2 in entries:
          p2 = f"{prefix}{delimiter}{k}"
          recurse_flatten(v2, p2)
    elif isinstance(v, list):
      if not v:
        flat_dict[prefix[1:]] = v
      else:
        for i, v2 in enumerate(v):
          p2 = f"{prefix}[{i}]"
          recurse_flatten(v2, p2)
    else:
      flat_dict[prefix[1:]] = v

  recurse_flatten(dic)
  return flat_dict

def parse_tree(flat_tree: str) -> List[Union[str, int]]:
  """Unflattens a flattened tree path."""
  for j, key in enumerate(tree := str(flat_tree).split('.')):
      # Avoid parsing literal array indices
      if isinstance(tree[j], int): continue
      # Insert array indices as additional keys
      elif (re_match := re_search(r'(.*)\[([0-9]+)\]', key, group=None)):
        key, idx = re_match.groups()
        tree[j] = key
        tree[j+1:j+1] = [int(idx)]

  return tree

def nested_get(dic: dict,
               keys: List[str],
               default: Optional[any]=None
               ) -> Union[dict, any, None]:
  """Retrieves a nested value from a dictionary.

  Args:
    dic: The dictionary to retrieve the value from.
    keys: The keys to traverse the dictionary.

  Returns:
    The value at the end of the keys list.
  """
  try:
    for key in keys:
      dic = dic[key]
    return dic
  except KeyError:
    return default

def nested_set(dic: dict,
               keys: List[str],
               value: any
               ) -> None:
  """Sets a nested value in a dictionary.

  Args:
    dic: The dictionary to set the value in.
    keys: The keys to traverse the dictionary.
    value: The value to set.
  """
  for key in keys[:-1]:
    if isinstance(dic, dict):
      dic = dic.setdefault(key, {})
    else: return
  dic[keys[-1]] = value

def nested_del(dic: dict,
               keys: List[str]
               ) -> None:
  """Deletes a nested value in a dictionary.

  Args:
    dic: The dictionary to delete the value from.
    keys: The keys to traverse the dictionary.
  """
  for key in keys[:-1]: dic = dic[key]
  del dic[keys[-1]]

def merge_dict(a: dict, b: dict) -> dict:
  """Merges two dictionaries recursively.

  Args:
    a: The first dictionary.
    b: The second dictionary.

  Returns:
    The merged dictionary.
  """
  def merge_recurse(a, b, path=None):
    # Recurse on dict entries' values
    if isinstance(a, dict) and isinstance(b, dict):
      # Compute set of all keys in both dictionaries
      keys = sorted(set(a.keys()) | set(b.keys()))
      # Build output dictionary, merging values with common keys recursively
      return { k: merge_recurse(a.get(k), b.get(k), path + [k]) for k in keys }
    # Append array values by default
    elif isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
      return a + b
    # Override values of `a` with `b` if present in both
    else: return a if b is None else b
  # Merge dictionaries
  return merge_recurse(a, b, path=[])


__all__ = [
  # Functions (6)
  "flatten_dict",
  "parse_tree",
  "nested_get",
  "nested_set",
  "nested_del",
  "merge_dict"
]
