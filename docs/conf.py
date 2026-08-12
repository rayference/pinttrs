import datetime

import pintext

# -- Project information -------------------------------------------------------

project = "Pintext"
copyright = f"2021-{datetime.datetime.now().year}, Rayference"  # noqa: DTZ005
author = "Vincent Leroy"
release = pintext.__version__
version = pintext.__version__

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
    "sphinx_design",
    "sphinx_iconify",
    "sphinx_autodoc_typehints",
]

source_suffix = [".rst", ".md"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Intersphinx options -------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "attrs": ("https://www.attrs.org/en/stable", None),
    "pint": ("https://pint.readthedocs.io/en/stable", None),
    "pydantic": ("https://docs.pydantic.dev/latest", None),
}

# -- GitHub quicklinks with 'extlinks' -----------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/extlinks.html

ghbase = "https://github.com"
ghroot = f"{ghbase}/rayference/pintext"
extlinks = {
    "ghissue": (f"{ghroot}/issues/%s", "GH%s"),
    "ghpr": (f"{ghroot}/pull/%s", "PR%s"),
    "ghcommit": (f"{ghroot}/commit/%s", "%.7s"),
    "ghuser": (f"{ghbase}/%s", "@%s"),
}

# -- Options for HTML output ---------------------------------------------------

html_static_path = ["_static"]
html_title = "Pintext"
html_show_sourcelink = False

# Use Shibuya theme
# https://shibuya.lepture.com/
html_theme = "shibuya"
html_theme_options = {
    "accent_color": "blue",
    "navigation_with_keys": True,
    "github_url": ghroot,
    # Note: Shibuya resolves logo paths relative to the documentation root,
    # unlike Furo which resolves them against html_static_path. File names are
    # keyed to ink colour: 'light_logo' is the logo displayed in light mode,
    # i.e. the dark-ink one.
    "light_logo": "_static/pintext-logo-black.svg",
    "dark_logo": "_static/pintext-logo-white.svg",
    "nav_links_align": "center",
    "nav_links": [
        {"title": "User guide", "url": "user_guide/index"},
        {"title": "Porting", "url": "porting"},
        {"title": "API", "url": "api/pintext"},
        {"title": "Contributing", "url": "dev/index"},
    ],
}
