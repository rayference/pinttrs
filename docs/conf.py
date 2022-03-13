# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import pinttr

# -- Path setup ----------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#

# sys.path.insert(0, os.path.abspath("../src"))

# -- Project information -------------------------------------------------------


project = "Pinttrs"
copyright = "2021, Rayference"
author = "Vincent Leroy"
release = pinttr.__version__
version = pinttr.__version__

# -- General configuration -----------------------------------------------------

extensions = [
    # Core extensions
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    # Third-party
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_autodoc_typehints",
]

templates_path = ["_templates"]
source_suffix = [".rst", ".md"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Intersphinx options -------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# -- GitHub quicklinks with 'extlinks' -----------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/extlinks.html

ghbase = "https://github.com"
ghroot = f"{ghbase}/leroyvn/pinttrs"
extlinks = {
    "ghissue": (f"{ghroot}/issues/%s", "GH%s"),
    "ghpr": (f"{ghroot}/pull/%s", "PR%s"),
    "ghcommit": (f"{ghroot}/commit/%s", "%.7s"),
    "ghuser": (f"{ghbase}/%s", "@%s"),
}

# -- Options for HTML output ---------------------------------------------------

html_static_path = ["_static"]
html_title = "Pinttrs"

# Use Furo theme
# https://pradyunsg.me/furo/
html_theme = "furo"
html_theme_options = {
    "navigation_with_keys": True,
    "sidebar_hide_name": True,
    "light_logo": "pinttrs_logo_dark.svg",
    "dark_logo": "pinttrs_logo_light.svg",
}
