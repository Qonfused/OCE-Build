# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from typing import Any, Dict

#pragma preserve-imports - Inject project namespaces into the module search path
import sys, pathlib; sys.path.insert(1, str(pathlib.Path(__file__, '../' * 4).resolve()))

from ci import PROJECT_ROOT

from ocebuild.version import __version__ as ocebuild_version

# -- Project information -------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "OCE Build"
copyright = "2023, The OCE Build Authors"
author = "Cory Bennett"
release = ocebuild_version

# -- General configuration -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
  # Sphinx extensions
  "sphinx.ext.autodoc",
  "sphinx.ext.extlinks",
  "sphinx.ext.intersphinx",
  "sphinx.ext.mathjax",
  "sphinx.ext.napoleon",
  "sphinx.ext.todo",
  "sphinx.ext.viewcode",
  # Third-party extensions
  "autoapi.extension",
  "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = []

source_suffix = {
  '.rst': 'restructuredtext',
  '.txt': 'markdown',
  '.md': 'markdown',
}

html_sidebars = {
  "**": [
    "sidebar/scroll-start.html",
    "sidebar/brand.html",
    "sidebar/search.html",
    "sidebar/navigation.html",
    "sidebar/ethical-ads.html",
    "sidebar/scroll-end.html",
  ]
}

# -- Options for extlinks ------------------------------------------------------

extlinks = {
  "pypi": ("https://pypi.org/project/%s/", "%s"),
}

# -- Options for HTML output ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_title = "OCE Build"
language   = "en"

html_static_path = ["_static"]
html_last_updated_fmt = ""

html_theme_options: Dict[str, Any] = {
  "footer_icons": [
    {
      "name": "GitHub",
      "url": "https://github.com/Qonfused/OCE-Build",
      "html": """
        <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
          <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
        </svg>
      """,
      "class": "",
    },
  ],
  "source_repository": "https://github.com/Qonfused/OCE-Build/",
  "source_branch": "main",
  "source_directory": "docs/",
}

# -- Options for autoapi -------------------------------------------------------

autoapi_dirs = [
  str(PROJECT_ROOT.joinpath('ci/tools/poetry/build/ocebuild')),
]
autoapi_ignore = [ "*_test.py" ]
autoapi_root = "api"
autoapi_template_dir = "_templates"
