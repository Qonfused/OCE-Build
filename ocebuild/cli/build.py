## @file
# Copyright (c) 2023, Cory Bennett. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
##
""""""

from ocebuild.filesystem import remove
from ocebuild.pipeline.build import read_build_config
from ocebuild.pipeline.lock import resolve_lockfile
from ocebuild.pipeline.opencore import extract_opencore_directory
from ocebuild.sources.resolver import PathResolver


if __name__ == '__main__':
  filepath = 'docs/example/build.yml'
  #TODO: Add an --outDir parameter
  out_dir = 'dist'
  #TODO: Add an --update flag
  update = False
  #TODO: Add a --force flag
  force = True
  #TODO: Add a --clean flag
  clean = False

  PARENT_DIR = PathResolver(filepath).parent
  BUILD_DIR = PARENT_DIR.joinpath(out_dir)
  LOCKFILE = PARENT_DIR.joinpath('build.lock')

  if clean: remove(BUILD_DIR)

  build_config, build_vars, flags = read_build_config(filepath)

  lockfile, resolvers = resolve_lockfile(build_config,
                                         lockfile_path=LOCKFILE,
                                         parent_dir=PARENT_DIR,
                                         update=update,
                                         force=force)

  # Extract the OpenCore package to the output directory
  OC_DIR = extract_opencore_directory(resolvers,
                                      lockfile,
                                      target=build_vars['variables']['target'],
                                      out_dir=BUILD_DIR)

  from pprint import pprint
  pprint(resolvers)
