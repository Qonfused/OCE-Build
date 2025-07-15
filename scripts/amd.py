## @file
# Patch script for generating AMD patches for macOS.
#
# Copyright (c) 2023-2025, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##

# /// script
# requires-python = ">=3.8"
# description = "Generate patches.yaml from AMD Vanilla and WMSR patches"
# dependencies = [
#   "click",
#   "ocebuild>=0.1.0.dev0",
# ]
# ///

import click
from ocebuild.filesystem import extract_archive
from ocebuild.parsers.yaml import write_yaml
from ocebuild.pipeline.config import read_config


AMD_PATCH_ARCHIVE = 'https://github.com/AMD-OSX/AMD_Vanilla/archive/refs/heads/master.zip'
WMSR_PATCH_ARCHIVE = 'https://github.com/user-attachments/files/18508274/patch.plist.zip'


@click.command()
@click.option('--cpu',
              required=True,
              type=int,
              help='Number of CPU cores for the WMSR patch')
@click.option('--hyperv',
              is_flag=True,
              help='Include WMSR patch for Hyper-V VMs')
@click.option('--out',
              default='patch.amd.yml',
              show_default=True,
              help='Output path for the generated YAML file')
def main(cpu, hyperv, out):
  with extract_archive(AMD_PATCH_ARCHIVE) as tmp_dir:
    plist_file = next(tmp_dir.glob('**/patches.plist'))
    amd_patches = write_yaml(read_config(plist_file), schema='annotated')
    amd_patches = "\n".join(amd_patches)\
      .replace('<B8000000 0000>', f'<B8{cpu:02X}0000 0000>')\
      .replace('<BA000000 0000>', f'<BA{cpu:02X}0000 0000>')\
      .replace('<BA000000 0090>', f'<BA{cpu:02X}0000 0090>')\
      .replace('<BA000000 00>',   f'<BA{cpu:02X}0000 00>')

  wmsr_patch = ''
  if hyperv:
    with extract_archive(WMSR_PATCH_ARCHIVE) as tmp_dir:
      plist_file = tmp_dir / 'patch.plist'
      wmsr_patch = write_yaml(read_config(plist_file), schema='annotated')
      wmsr_patch = "\n".join(wmsr_patch)

  with open(out, 'w') as f:
    f.write(f"""\
# AMD Patches
# - Required as AMD does not have a native power management driver in macOS.
Kernel:
  Emulate:
    DummyPowerManagement: Boolean | true

# AMD Vanilla Patches
# - {AMD_PATCH_ARCHIVE.split('/archive/')[0]}
{amd_patches}

""")
    if hyperv:
      f.write(f"""\
# WMSR Patch
# - Required for OS X 10.13+ (High Sierra) in Hyper-V VMs
# - Refer to https://github.com/Qonfused/OSX-Hyper-V
{wmsr_patch}
""")

if __name__ == '__main__':
  main()
