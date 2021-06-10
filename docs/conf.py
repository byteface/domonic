# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
import domonic

# -- Project information -----------------------------------------------------

project = 'domonic'
copyright = '2021, byteface'
author = 'byteface'

# The full version, including alpha/beta/rc tags
release = domonic.__version__ #'0.2.17'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon"
]

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

html_theme_options = {
    "show_powered_by": False,
    "github_user": "byteface",
    "github_repo": "domonic",
    "github_banner": True,
    "show_related": False,
    "note_bg": "#FFF59C",
}

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
html_use_smartypants = False

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {
#    "index": ["sidebarintro.html", "sourcelink.html", "searchbox.html", "hacks.html"],
#    "**": [
#        "sidebarlogo.html",
#        "localtoc.html",
#        "relations.html",
#        "sourcelink.html",
#        "searchbox.html",
#        "hacks.html",
#    ],
#}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

master_doc = 'index'

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "urllib3": ("https://urllib3.readthedocs.io/en/latest", None),
}
