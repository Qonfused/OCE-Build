#!/usr/bin/env python3

## @file
# Copyright (c) 2026, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
"""Tests for the lock command."""

from types import SimpleNamespace

from rich.markup import render

from .lock import rich_resolver


def test_rich_resolver_handles_generated_path_name():
  """Generated artifacts may not share the source specifier's filename."""
  resolution = \
    'SSDT-ALS0@file:ACPI/SSDT-ALS0.dsl#checksum=abc123'
  resolver = SimpleNamespace(path='ACPI/SSDT-ALS0.aml')

  formatted = rich_resolver(resolver, {'path': resolver.path}, resolution)

  assert render(formatted).plain == resolution


def test_rich_resolver_escapes_path_markup():
  """Path text containing Rich markup syntax must remain literal."""
  resolution = \
    'Example@file:Kexts/[release]/Example.kext#checksum=abc123'
  resolver = SimpleNamespace(path='Kexts/[release]/Example.kext')

  formatted = rich_resolver(resolver, {'path': resolver.path}, resolution)

  assert render(formatted).plain == resolution
