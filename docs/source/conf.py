from pathlib import Path
from importlib import import_module
import inspect


# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath("../../"))

# -- Project information -----------------------------------------------------

import ts2vg

project = "ts2vg"
copyright = "2023, Carlos Bergillos"
author = "Carlos Bergillos"
release = ts2vg.__version__
version = ts2vg.__version__


# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.githubpages",
    "sphinx.ext.mathjax",
    "sphinx.ext.linkcode",
    "sphinx.ext.autosummary",
]

autoclass_content = "class"
autodoc_member_order = "bysource"
autodoc_typehints = "none"
napoleon_use_rtype = False

templates_path = ["_templates"]

exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

html_theme = "pydata_sphinx_theme"

html_static_path = ["_static"]

html_css_files = [
    "custom.css",
]

html_copy_source = False
html_show_sourcelink = False

html_favicon = "_static/favicon-32x32.png"

html_theme_options = {
    "favicons": [
        {
            "rel": "icon",
            "sizes": "16x16",
            "href": "favicon-16x16.png",
        },
        {
            "rel": "icon",
            "sizes": "32x32",
            "href": "favicon-32x32.png",
        },
    ],
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/CarlosBergillos/ts2vg",
            "icon": "fab fa-github",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/ts2vg",
            "icon": "fas fa-cube",
        },
    ],
    "show_prev_next": False,
    "navigation_with_keys": False,
}

# svg math output
# mathjax_path = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"


# -- Options for sphinx.ext.autosummary --------------------------------------

autosummary_generate = True
autosummary_imported_members = True


# -- Options for sphinx.ext.linkcode -----------------------------------------


def linkcode_resolve(domain, info):
    if domain != "py":
        return None
    if not info["module"]:
        return None

    module = import_module(info["module"])
    obj = module
    for attr in info["fullname"].split("."):
        if not hasattr(obj, attr):
            return None

        obj = getattr(obj, attr)

    if isinstance(obj, property):
        obj = obj.fget

    module_path = Path(inspect.getsourcefile(module)).parent
    source_file = Path(inspect.getsourcefile(obj))
    source, source_line_from = inspect.getsourcelines(obj)
    source_line_to = source_line_from + len(source) - 1

    relative_path = module_path.name / source_file.relative_to(module_path)

    return f"https://github.com/CarlosBergillos/ts2vg/blob/main/{relative_path}#L{source_line_from}-L{source_line_to}"
