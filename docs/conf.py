import datetime

import pinttrs

# -- Project information -------------------------------------------------------

project = "Pinttrs"
copyright = f"2021-{datetime.datetime.now().year}, Rayference"
author = "Vincent Leroy"
release = pinttrs.__version__
version = pinttrs.__version__

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
    "attrs": ("https://www.attrs.org/en/stable", None),
    "pint": ("https://pint.readthedocs.io/en/stable", None),
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
