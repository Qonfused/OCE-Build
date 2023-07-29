## @file
# Copyright (c) 2023, The OCE Build Authors. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

from collections import OrderedDict
from functools import partial

import pytest

from .asl import *
from .regex import re_search

from ci import PROJECT_EXAMPLES


SIMPLE_DEMO = PROJECT_EXAMPLES.joinpath('simple-demo-project', 'src')

################################################################################
#                              Regular Expressions                             #
################################################################################

def test_RE_BLOCK_ARGS():
  regex_fn = partial(re_search,
                     pattern=RE_BLOCK_ARGS,
                     group=1,
                     multiline=True)
  assert regex_fn(string='Method ("Name", 0, "Serialized") {}') == \
    '"Name", 0, "Serialized"'

  assert regex_fn(string='DefinitionBlock ("", "SSDT", 2, "SSDTA", "TEST", 0x00000000)') == \
    '"", "SSDT", 2, "SSDTA", "TEST", 0x00000000'

def test_RE_IMPORT_TYPE():
  regex_fn = partial(re_search,
                     pattern=RE_IMPORT_TYPE,
                     group=None,
                     multiline=True)
  assert regex_fn(string='External (\\_SB.FOO.BAR, DeviceObj)'
                  ).groups() == \
    ('DeviceObj',)

def test_RE_LOCAL_VAR():
  regex_fn = partial(re_search,
                     pattern=RE_LOCAL_VAR,
                     group=None,
                     multiline=True)
  assert regex_fn(string='Arg22').groups() == \
    ('Arg',
     '22')
  assert regex_fn(string='Local0').groups() == \
    ('Local',
     '0')

def test_RE_STATEMENT():
  regex_fn = partial(re_search,
                     pattern=RE_STATEMENT,
                     group=None,
                     multiline=True)
  # Handle example use cases
  assert regex_fn(string='Device (_SB.PCI0.GFX0.PNLF)'
                  ).groups() == \
    ('Device', '_SB.PCI0.GFX0.PNLF')
  assert regex_fn(string='Method (_Q0E, 0, NotSerialized)'
                  ).groups() == \
    ('Method', '_Q0E')
  assert regex_fn(string='Name (SPBL, Buffer (0x02) { 0x01, 0xFF })'
                  ).groups() == \
    ('Name', 'SPBL')
  # Handle edge cases
  assert regex_fn(string='Name(Arg22, Buffer (0x02) { 0x01, 0xFF })'
                  ).groups() == \
    ('Name', 'Arg22')
  assert not regex_fn(string='Arg22 = Buffer (0x02) { 0x01, 0xFF }')

def test_RE_NAME():
  regex_fn = partial(re_search,
                     pattern=RE_NAME,
                     multiline=True)
  # Handle example use cases
  assert not regex_fn(string='0xFF00BAZ')
  assert not regex_fn(string='iNVALID')
  assert regex_fn(string='\\_SB.FOO_._BAR') == '\\_SB.FOO_._BAR'

################################################################################
#                              ASL Parsing Methods                             #
################################################################################

def test_parse_definition_block():
  string = 'DefinitionBlock ("", "DSDT", 2, "_ASUS_", "Notebook", 0x01072009)'
  assert parse_definition_block(string) == \
    OrderedDict([('AMLFileName', ''),
                  ('TableSignature', 'DSDT'),
                  ('ComplianceRevision', 2),
                  ('OEMID', 'ASUS'),
                  ('TableID', 'Notebook'),
                  ('OEMRevision', '0x01072009')])
  # Throws error on invalid definition block
  with pytest.raises(ValueError):
    parse_definition_block('DefinitionBlock ()')

def test_parse_ssdt_namespace():
  # Test against SSDT-A
  with open(f'{SIMPLE_DEMO}/ACPI/SSDT-A.dsl', encoding='UTF-8') as ssdt_file:
    assert parse_ssdt_namespace(ssdt_file) == \
      {'definition_block': OrderedDict([('AMLFileName', ''),
                                        ('TableSignature', 'SSDT'),
                                        ('ComplianceRevision', 2),
                                        ('OEMID', 'SSDTA'),
                                        ('TableID', 'TEST'),
                                        ('OEMRevision', '0x00000000')]),
      'imports': OrderedDict([('SB', 'DeviceObj'),
                              ('SB.PCI0', 'DeviceObj')]),
      'statements': OrderedDict([('QUX', 'Name'),
                                 ('SB.BAZ', 'Device'),
                                 ('SB.BAZ.HID', 'Name'),
                                 ('SB.PCI0.QUUX', 'Name')])}

  # Test against SSDT-B
  with open(f'{SIMPLE_DEMO}/ACPI/SSDT-B.dsl', encoding='UTF-8') as ssdt_file:
    assert parse_ssdt_namespace(ssdt_file) == \
      {'definition_block': OrderedDict([('AMLFileName', ''),
                                        ('TableSignature', 'SSDT'),
                                        ('ComplianceRevision', 2),
                                        ('OEMID', 'SSDTB'),
                                        ('TableID', 'TEST'),
                                        ('OEMRevision', '0x00000000')]),
      'imports': OrderedDict([('SB', 'DeviceObj'),
                              ('SB.PCI0.FIZ', 'DeviceObj'),
                              ('SB.BAZ', 'DeviceObj')]),
      'statements': OrderedDict([('SB.BAR', 'Device'),
                                 ('FUUB', 'Name'),
                                 ('SB.FOO', 'Device'),
                                 ('SB.FOO.XUUQ', 'Name'),
                                 ('BUUF', 'Name'),
                                 ('BUUX', 'Name')])}
