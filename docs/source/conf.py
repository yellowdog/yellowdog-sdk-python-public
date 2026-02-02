# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from datetime import date
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join('..', '..')))
import yellowdog_client
doc_name = u'YellowDog Client Documentation'

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "yellowdog-sdk"
author = "YellowDog Limited"
copyright = f"{date.today().year}, YellowDog Limited. Version {yellowdog_client.__version__}"
version = yellowdog_client.__version__
release = yellowdog_client.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx_autodoc_typehints',
    'sphinx_automodapi.smart_resolver'
]

# Options for highlighting
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-highlighting
pygments_style = 'sphinx'

# Options for internationalisation
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-internationalisation
language = 'en'

# Options for source files
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-source-files
exclude_patterns = []
master_doc = 'index'
source_suffix = '.rst'

# Options for templating
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-templating
templates_path = ['_templates']

# -- Builder options ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#builder-options


# Options for HTML output
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_css_files = [
    'css/yellowdog.css',
    'https://fonts.googleapis.com/css2?family=Mulish:wght@300;400;600;700&family=Roboto:wght@300;400;500;700&display=swap'
]
html_logo = '_static/yellowdog.svg'
html_static_path = ['_static']
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'style_nav_header_background': '#FAB842',
}

# Options for HTMLHelp output
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-help-output
htmlhelp_basename = 'YellowDogClientdoc'

# Options for Epub output
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-epub-output
epub_exclude_files = ['search.html']
epub_title = project # TODO This is the default, can we get rid?

# Options for LaTeX output
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-latex-output
latex_documents = [
    (master_doc, 'YellowDogClient.tex', doc_name,
     u'YellowDog Limited', 'manual'),
]
latex_elements = { }

# Options for manual page output
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-manual-page-output
man_pages = [ (master_doc, 'yellowdogclient', doc_name, [author], 1) ]

# Options for Texinfo output
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-texinfo-output
texinfo_documents = [ (master_doc, 'YellowDogClient', u'YellowDog Client Documentation', author, 'YellowDogClient', 'One line description of project.', 'Miscellaneous') ]

# -- Extension configuration -------------------------------------------------

# Autodoc
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
autodoc_inherit_docstrings = True

# Intersphinx
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}

# sphinx-autodoc-typehints
# https://github.com/tox-dev/sphinx-autodoc-typehints
always_document_param_types = True