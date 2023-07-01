## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Methods for retrieving and handling Kext packages."""

from contextlib import contextmanager
from shutil import rmtree

from typing import Generator, Literal, Union

from ocebuild.filesystem.archives import extract_archive
from ocebuild.parsers.dict import nested_get
from ocebuild.parsers.plist import parse_plist
from ocebuild.sources.github import github_release_catalog
from ocebuild.sources.resolver import GitHubResolver, DortaniaResolver, PathResolver


@contextmanager
def extract_kext_archive(url: str,
                         persist: bool=False
                         ) -> Generator[dict, any, None]:
  """Extracts Kexts from a URL and yields a temporary extraction dictionary.

  Args:
    url: URL of the archive file.
    persist: Flag to disable cleanup of the temporary directory.

  Yields:
    kexts (dict): Dictionary of extracted kexts.

  Example:
    >>> with extract_kexts('https://example.com/foo.zip') as kexts:
    ...   print(kexts)
    # -> {
    #   'Foo': {
    #     '__extract': './Foo.kext'
    #     '__path': Path('/tmp/foo/Foo.kext'),
    #     '__url': 'https://example.com/foo.zip',
    #     'identifier': 'com.example.foo',
    #     'version': '1.0.0',
    #     'dependencies': {
    #       'com.example.bar': '1.0.0'
    #     }
    #   },
    #   'Bar': { ... }
    # }
  """
  kexts = dict()
  try:
    with extract_archive(url, persist=True) as pkg:
      for plist_path in pkg.glob('**/*.kext/Contents/Info.plist'):
        kext_path = PathResolver(plist_path).parents[1].as_posix()
        extract_path = f'.{str(kext_path)[len(str(pkg)):]}'
        with open(plist_path, 'r', encoding='UTF-8') as file:
          # Build plist dictionary from filestream
          plist = parse_plist(file)
          # Extract Kext bundle properties
          name = plist['CFBundleName'][1]
          identifier = plist['CFBundleIdentifier'][1]
          version = plist['CFBundleVersion'][1]
          executable = plist['CFBundleExecutable'][1]
          libraries = { k:v[1] for k,v in plist['OSBundleLibraries'].items()
                            # Ignore self-dependencies
                        if (not k == identifier and
                            # Ignore Apple-provided libraries
                            not k.startswith('com.apple.')) }
          # Cleanup
          del plist
        # Update kext dictionary
        kexts[name] = {
          "__extract": extract_path,
          "__path": kext_path,
          "__url": url,
          "identifier": identifier,
          "version": version,
          "executable": executable,
          "dependencies": libraries
        }
    # Yield the kexts dictionary.
    yield kexts
  finally:
    # Cleanup after context exits
    if not persist: rmtree(pkg)

def extract_kext_release(resolver: Union[GitHubResolver, DortaniaResolver],
                         build: Literal['RELEASE', 'DEBUG']='RELEASE'
                         ):
  name = resolver.__name__
  url = resolver.resolve()
  if '/releases/' not in url:
    raise ValueError(f'URL must resolve to a GitHub release.')

  # Get the release catalog for a given release url
  release_catalog = github_release_catalog(url)
  assets = release_catalog['assets']
  if not len(assets):
    raise ValueError(f'Release catalog for {name} has no assets.')
  # Return the first release if only 1 artifact is present
  elif len(assets) == 1:
    return nested_get(assets, [0, 'browser_download_url'])
  
  has_name = lambda asset: all([ s in asset['name'] for s in name.split('-') ])
  has_build = lambda asset: build in asset['name']
  # Handle case where there is no clear resolution of the desired kext
  if arr := list(filter(lambda a: not (has_name(a) and has_build(a)), assets)):
    pass
  # Handle ambiguous build targets
  elif arr := list(filter(lambda a: has_name(a) and not has_build(a), assets)):
    pass
  #
  elif arr := list(filter(lambda a: has_name(a) and not has_build(a), assets)):
    pass

__all__ = [
  "extract_kext_archive",
  "extract_kext_release"
]
