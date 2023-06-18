## @file
# Dictionary helper functions.
#
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##


def flattenDict(dic: dict):
  flat_dict: dict={}
  def recurse_flatten(v: any, prefix=''):
    match v:
      case dict():
        for k, v2 in v.items():
          p2 = "{}.{}".format(prefix, k)
          recurse_flatten(v2, p2)
      case list():
        for i, v2 in enumerate(v):
          p2 = "{}[{}]".format(prefix, i)
          recurse_flatten(v2, p2)
      case _:
        flat_dict[prefix[1:]] = v
  recurse_flatten(dic)
  return flat_dict

def nestedGet(dic: dict, keys: list[str]) -> dict | None:
  """Retrieves a nested value from a dictionary.

  Args:
    dic (dict): The dictionary to retrieve the value from.
    keys (list): The keys to traverse the dictionary.

  Returns:
    The value at the end of the keys list.
  """
  try:
    for key in keys: dic = dic[key]
    return dic
  except: return

def nestedSet(dic: dict, keys: list[str], value: any):
  """Sets a nested value in a dictionary.

  Args:
    dic (dict): The dictionary to set the value in.
    keys (list): The keys to traverse the dictionary.
    value (any): The value to set.
  """
  for key in keys[:-1]:
    if isinstance(dic, dict):
      dic = dic.setdefault(key, {})
    else: return
  dic[keys[-1]] = value

def nestedDel(dic: dict, keys: list[str]):
  """Deletes a nested value in a dictionary.

  Args:
    dic (dict): The dictionary to delete the value from.
    keys (list): The keys to traverse the dictionary.
  """
  for key in keys[:-1]: dic = dic[key]
  del dic[keys[-1]]
