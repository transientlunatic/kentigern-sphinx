"""
kentigern.ext.steps
===================

A pair of Sphinx directives for authoring numbered, visually-connected
tutorial steps.

Usage in reStructuredText::

    .. steps::

       .. step:: Set Up Your Environment

          Create a conda environment named ``my-env``::

              conda create -n my-env python=3.11
              conda activate my-env

       .. step:: Install Dependencies

          Install the required packages::

              pip install my-package

The ``steps`` directive is a container; all ``step`` children inside it are
automatically numbered via a CSS counter (no Python-side bookkeeping needed).
A ``step`` directive can also be used outside a ``steps`` container, in which
case it renders as step 1 of an implicit list.

To activate this extension, add it to your Sphinx ``conf.py``::

    extensions = ["kentigern.ext.steps"]

When the ``kentigern`` theme is active this extension is registered
automatically.
"""

from docutils import nodes
from sphinx.util.docutils import SphinxDirective

__all__ = ["setup"]


# ---------------------------------------------------------------------------
# Custom docutils nodes
# ---------------------------------------------------------------------------

class steps_container(nodes.General, nodes.Element):
    """Wrapper node for a numbered-step sequence."""


class step_node(nodes.General, nodes.Element):
    """A single step within a ``steps_container`` (or standalone)."""


class step_title(nodes.TextElement):
    """The title line of a ``step_node``."""


# ---------------------------------------------------------------------------
# HTML visit / depart functions
# ---------------------------------------------------------------------------

def visit_steps_container_html(self, node):
    self.body.append('<div class="kentigern-steps">\n')


def depart_steps_container_html(self, node):
    self.body.append('</div>\n')


def visit_step_node_html(self, node):
    self.body.append('<div class="kentigern-step">\n')
    # Left column: circle (::before CSS counter) + connector line
    self.body.append(
        '<div class="kentigern-step__marker">'
        '<div class="kentigern-step__connector"></div>'
        '</div>\n'
    )
    # Right column: title + body content
    self.body.append('<div class="kentigern-step__content">\n')


def depart_step_node_html(self, node):
    self.body.append('</div>\n')  # close kentigern-step__content
    self.body.append('</div>\n')  # close kentigern-step


def visit_step_title_html(self, node):
    self.body.append('<p class="kentigern-step__title">')


def depart_step_title_html(self, node):
    self.body.append('</p>\n')


# ---------------------------------------------------------------------------
# LaTeX / plain-text fall-throughs
# ---------------------------------------------------------------------------

def _noop_visit(self, node):
    pass


def _noop_depart(self, node):
    pass


def _latex_visit_step_node(self, node):
    # Emit a bold title in square brackets then a list environment.
    self.body.append('\n\\begin{description}\n')


def _latex_depart_step_node(self, node):
    self.body.append('\\end{description}\n')


def _latex_visit_step_title(self, node):
    self.body.append('\\item[')


def _latex_depart_step_title(self, node):
    self.body.append('] ')


# ---------------------------------------------------------------------------
# Directives
# ---------------------------------------------------------------------------

class StepsDirective(SphinxDirective):
    """Container that wraps one or more ``step`` directives."""

    has_content = True
    required_arguments = 0
    optional_arguments = 0

    def run(self):
        self.assert_has_content()
        container = steps_container()
        self.state.nested_parse(self.content, self.content_offset, container)
        return [container]


class StepDirective(SphinxDirective):
    """A single numbered step.

    The optional argument becomes the step title::

        .. step:: Title of This Step

           Body content goes here.
    """

    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True

    def run(self):
        node = step_node()

        if self.arguments:
            title = step_title(text=self.arguments[0])
            title += nodes.Text(self.arguments[0])
            node += title

        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


# ---------------------------------------------------------------------------
# Extension entry point
# ---------------------------------------------------------------------------

def setup(app):
    """Register nodes, directives, and static assets with Sphinx."""

    app.add_node(
        steps_container,
        html=(visit_steps_container_html, depart_steps_container_html),
        latex=(_noop_visit, _noop_depart),
        text=(_noop_visit, _noop_depart),
    )
    app.add_node(
        step_node,
        html=(visit_step_node_html, depart_step_node_html),
        latex=(_latex_visit_step_node, _latex_depart_step_node),
        text=(_noop_visit, _noop_depart),
    )
    app.add_node(
        step_title,
        html=(visit_step_title_html, depart_step_title_html),
        latex=(_latex_visit_step_title, _latex_depart_step_title),
        text=(_noop_visit, _noop_depart),
    )

    app.add_directive("steps", StepsDirective)
    app.add_directive("step", StepDirective)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
