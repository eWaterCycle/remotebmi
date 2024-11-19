# remotebmi documentation build configuration file
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.
from pathlib import Path

import tomli

# -- General configuration ------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "myst_nb",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "autoapi.extension",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = [".rst"]

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "remotebmi"
copyright = "2024, Netherlands eScience Center"  # noqa: A001
author = "Stefan Verhoeven"


# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
# The full version, including alpha/beta/rc tags.
def get_version():
    """Get the version from pyproject.toml."""
    # Not using importlib as we do not want to install
    # package during readthdocs build, to keep build quick
    project = Path(__file__).parent / "../pyproject.toml"
    with project.open("rb") as f:
        pyproject = tomli.load(f)
        return pyproject["project"]["version"]


version = get_version()
release = version

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
# TODO move logo to root of docs folder, also some notebooks will need to be updated
html_logo = "examples/logo.png"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
html_sidebars = {
    "**": [
        "relations.html",  # needs 'show_related': True theme option to display
        "searchbox.html",
    ]
}


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "remotebmi_doc"


# -- Options for LaTeX output ---------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        "remotebmi.tex",
        "remotebmi Documentation",
        "Stefan Verhoeven",
        "manual",
    ),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "remotebmi", "remotebmi Documentation", [author], 1)]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "remotebmi",
        "remotebmi Documentation",
        author,
        "remotebmi",
        "Python utilities to gather input files for running a hydrology model",
        "Miscellaneous",
    ),
]

# Turned off nitpicky as not all warnings are fixable
# To find reference target not found warnings turn this on
nitpicky = False

autodoc_mock_imports = [
    "cf_units",  # Causes many errors in docs build.
]
# Prevent alphabetic sorting of (@data)class attributes/methods
autodoc_member_order = "bysource"

autoapi_dirs = ["../src"]
autoapi_python_class_content = "both"
autoapi_options = ["members", "undoc-members", "imported-members", "show-inheritance"]
# If you get build errors pointing to audoapi/**/*.rst files,
# to debug set `autoapi_keep_files` to True
autoapi_keep_files = False

myst_heading_anchors = 3
nb_execution_mode = "off"
nb_output_stderr = "remove"

intersphinx_mapping = {
    "cf_units": ("https://cf-units.readthedocs.io/en/latest/", None),
    "esmvalcore": ("https://docs.esmvaltool.org/projects/ESMValCore/en/latest/", None),
    "esmvaltool": ("https://docs.esmvaltool.org/en/latest/", None),
    "grpc4bmi": ("https://grpc4bmi.readthedocs.io/en/latest/", None),
    "iris": ("https://scitools-iris.readthedocs.io/en/latest/", None),
    "lime": ("https://lime-ml.readthedocs.io/en/latest/", None),
    "basic_modeling_interface": ("https://bmi.readthedocs.io/en/latest/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/dev", None),
    "python": ("https://docs.python.org/3/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
    "seaborn": ("https://seaborn.pydata.org/", None),
    "sklearn": ("https://scikit-learn.org/stable", None),
    "xarray": ("https://docs.xarray.dev/en/stable/", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
}

# Dont copy line number, >>> and ... from code blocks
copybutton_exclude = ".linenos, .gp"
