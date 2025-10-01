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
import reporter.types as reporter_types

sys.path.insert(0, os.path.abspath(".."))


# -- Project information -----------------------------------------------------

project = "python-reporter"
copyright = "2022, DongIT"
author = "Alexander Krigsman"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

autodoc_typehints = "description"

autodoc_type_aliases = dict()
for name in reporter_types.__all__:
    autodoc_type_aliases[name] = name
    autodoc_type_aliases[f"reporter.types.{name}"] = name

autodoc_default_options = {
    "members": True,
    "show-inheritance": True,
}

always_document_param_types = True

html_theme_options = {
    "collapse_navigation": False,
}


html_favicon = "_static/favicon.ico"


# List of type aliases that should be cross-referenced


def resolve_type_aliases(app, env, node, contnode):
    """Resolve :class: references to our type aliases as :data: instead.

    This is a workaround for https://github.com/sphinx-doc/sphinx/issues/10785
    where autodoc generates py:data entries for TypeAlias definitions, but
    type annotations try to resolve them as py:class references.
    """
    if (
        node["refdomain"] == "py"
        and node["reftype"] == "class"
        and node["reftarget"] in reporter_types.__all__
    ):
        # Try to resolve as py:data instead
        return app.env.get_domain("py").resolve_xref(
            env, node["refdoc"], app.builder, "data", node["reftarget"], node, contnode
        )


def setup(app):
    """Setup function for Sphinx extension."""
    app.connect("missing-reference", resolve_type_aliases)
