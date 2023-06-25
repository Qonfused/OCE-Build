## @file
# Dictionary helper functions.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

from typing import Dict, List, Union


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
      if not len(entries := v.items()):
        flat_dict[prefix[1:]] = ('dict', v)
      else:
        for k, v2 in entries:
          p2 = f"{prefix}{delimiter}{k}"
          recurse_flatten(v2, p2)
    elif isinstance(v, list):
      if not len(v):
        flat_dict[prefix[1:]] = ('list', v)
      else:
        for i, v2 in enumerate(v):
          p2 = f"{prefix}[{i}]"
          recurse_flatten(v2, p2)
    else:
      flat_dict[prefix[1:]] = v

  recurse_flatten(dic)
  return flat_dict

def nested_get(dic: dict,
               keys: List[str]
               ) -> Union[dict, None]:
  """Retrieves a nested value from a dictionary.

  Args:
    dic: The dictionary to retrieve the value from.
    keys: The keys to traverse the dictionary.

  Returns:
    The value at the end of the keys list.
  """
  try:
    for key in keys: dic = dic[key]
    return dic
  except: return None

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
