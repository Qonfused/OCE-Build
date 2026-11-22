## @file
# Copyright (c) 2026, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

from copy import copy
import json
from runpy import run_path
from types import SimpleNamespace

from packaging.version import Version
import pytest


@pytest.mark.parametrize('tag,expected', [
  ('v0.2.0', '0.2.0'),
  ('v0.2.0-rc.1', '0.2.0rc1'),
  ('v0.2.0+gabc123', '0.2.0+gabc123'),
])
def test_release_version_updates_package_metadata(tmp_path, monkeypatch,
                                                tag, expected):
  from ci.scripts import bump_version as bump

  version_file = tmp_path / 'ocebuild/version.py'
  version_file.parent.mkdir()
  version_file.write_bytes(bump.__version_file__.read_bytes())
  project = tmp_path / 'pyproject.toml'
  project.write_text(f'[tool.poetry]\nversion = "{bump.__version__}"\n',
                     encoding='utf-8')
  registry = tmp_path / 'ci/registry/project.json'
  registry.parent.mkdir(parents=True)
  monkeypatch.setattr(bump, 'PROJECT_ROOT', tmp_path)
  monkeypatch.setattr(bump, '__version_file__', version_file)
  monkeypatch.setattr(bump, 'version', copy(bump.version))

  bump._main(version_string=tag)

  metadata = run_path(str(version_file))
  assert metadata['__version__'] == expected
  assert f'version = "{expected}"' in project.read_text(encoding='utf-8')
  assert json.loads(registry.read_text())['version'] == expected
  components = SimpleNamespace(
    major=metadata['_MAJOR_VERSION'], minor=metadata['_MINOR_VERSION'],
    patch=metadata['_PATCH_VERSION'], pre_release=metadata['_PRE_RELEASE'],
    build=metadata['_BUILD'])
  assert Version(bump.format_version(components)) == Version(expected)
