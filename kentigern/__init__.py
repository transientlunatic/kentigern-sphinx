"""
Sphinx kentigern theme.

This theme borrows elements from the sphinx_bootstrap theme (of which it was originally a fork)
and the pydata sphinx theme.

"""
import os
from sphinx.errors import ExtensionError
from .bootstrap_html_translator import BootstrapHTML5Translator
import docutils


VERSION = (0, 1, 4)

__version__ = ".".join(str(v) for v in VERSION)
__version_full__ = __version__

def get_html_theme_path():
    """Return list of HTML theme paths."""
    theme_path = os.path.abspath(os.path.dirname(__file__))
    return [theme_path]

def add_toctree_functions(app, pagename, templatename, context, doctree):
    """Add functions so Jinja templates can add toctree objects.
    This converts the docutils nodes into a nested dictionary that Jinja can
    use in our templating.
    """
    from sphinx.environment.adapters.toctree import TocTree

    def get_nav_object(maxdepth=None, collapse=True, **kwargs):
        """Return a list of nav links that can be accessed from Jinja.
        Parameters
        ----------
        maxdepth: int
            How many layers of TocTree will be returned
        collapse: bool
            Whether to only include sub-pages of the currently-active page,
            instead of sub-pages of all top-level pages of the site.
        kwargs: key/val pairs
            Passed to the `TocTree.get_toctree_for` Sphinx method
        """
        # The TocTree will contain the full site TocTree including sub-pages.
        # "collapse=True" collapses sub-pages of non-active TOC pages.
        # maxdepth controls how many TOC levels are returned
        toctree = TocTree(app.env).get_toctree_for(
            pagename, app.builder, collapse=collapse, maxdepth=maxdepth, **kwargs
        )
        # If no toctree is defined (AKA a single-page site), skip this
        if toctree is None:
            return []

        # toctree has this structure
        #   <caption>
        #   <bullet_list>
        #       <list_item classes="toctree-l1">
        #       <list_item classes="toctree-l1">
        # `list_item`s are the actual TOC links and are the only thing we want
        toc_items = [
            item
            for child in toctree.children
            for item in child
            if isinstance(item, docutils.nodes.list_item)
        ]

        # Now convert our docutils nodes into dicts that Jinja can use
        nav = [docutils_node_to_jinja(child, only_pages=True) for child in toc_items]

        return nav

    def get_page_toc_object():
        """Return a list of within-page TOC links that can be accessed from Jinja."""
        self_toc = TocTree(app.env).get_toc_for(pagename, app.builder)

        try:
            # If there's only one child, assume we have a single "title" as top header
            # so start the TOC at the first item's children (AKA, level 2 headers)
            if len(self_toc.children) == 1:
                nav = docutils_node_to_jinja(self_toc.children[0]).get("children", [])
            else:
                nav = [docutils_node_to_jinja(item) for item in self_toc.children]
            return nav
        except Exception:
            return {}

    def navbar_align_class():
        """Return the class that aligns the navbar based on config."""
        align = context.get("theme_navbar_align", "content")
        align_options = {
            "content": ("col-lg-9", "mr-auto"),
            "left": ("", "mr-auto"),
            "right": ("", "ml-auto"),
        }
        if align not in align_options:
            raise ValueError(
                (
                    "Theme optione navbar_align must be one of"
                    f"{align_options.keys()}, got: {align}"
                )
            )
        return align_options[align]

    context["get_nav_object"] = get_nav_object
    context["get_page_toc_object"] = get_page_toc_object
    context["navbar_align_class"] = navbar_align_class


def docutils_node_to_jinja(list_item, only_pages=False):
    """Convert a docutils node to a structure that can be read by Jinja.
    Parameters
    ----------
    list_item : docutils list_item node
        A parent item, potentially with children, corresponding to the level
        of a TocTree.
    only_pages : bool
        Only include items for full pages in the output dictionary. Exclude
        anchor links (TOC items with a URL that starts with #)
    Returns
    -------
    nav : dict
        The TocTree, converted into a dictionary with key/values that work
        within Jinja.
    """
    if not list_item.children:
        return None

    # We assume this structure of a list item:
    # <list_item>
    #     <compact_paragraph >
    #         <reference> <-- the thing we want
    reference = list_item.children[0].children[0]
    title = reference.astext()
    url = reference.attributes["refuri"]
    active = "current" in list_item.attributes["classes"]

    # If we've got an anchor link, skip it if we wish
    if only_pages and "#" in url:
        return None

    # Converting the docutils attributes into jinja-friendly objects
    nav = {}
    nav["title"] = title
    nav["url"] = url
    nav["active"] = active

    # Recursively convert children as well
    # If there are sub-pages for this list_item, there should be two children:
    # a paragraph, and a bullet_list.
    nav["children"] = []
    if len(list_item.children) > 1:
        # The `.children` of the bullet_list has the nodes of the sub-pages.
        subpage_list = list_item.children[1].children
        for sub_page in subpage_list:
            child_nav = docutils_node_to_jinja(sub_page, only_pages=only_pages)
            if child_nav is not None:
                nav["children"].append(child_nav)
    return nav




def setup(app):
    """Setup."""
    theme_path = get_html_theme_path()[0]
    
    app.add_html_theme("kentigern", theme_path)
    app.set_translator("html", BootstrapHTML5Translator)    
    app.connect("html-page-context", add_toctree_functions)
