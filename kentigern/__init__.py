"""
Sphinx kentigern theme.

This theme borrows elements from the sphinx_bootstrap theme (of which it was originally a fork)
and the pydata sphinx theme.

"""
import os
from sphinx.errors import ExtensionError
import docutils


VERSION = (0, 1, 6)

__version__ = ".".join(str(v) for v in VERSION)
__version_full__ = __version__

def get_html_theme_path():
    """Return list of HTML theme paths."""
    theme_path = os.path.abspath(os.path.dirname(__file__))
    return [theme_path]


def setup(app):
    """Setup."""
    theme_path = get_html_theme_path()[0]
    
    app.add_html_theme("kentigern", theme_path)
    app.connect("html-page-context", add_toctree_functions)
