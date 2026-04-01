=========
Kentigern
=========

Kentigern is a modern Sphinx_ HTML theme built on Bootstrap 5.
It provides a three-column layout (site-wide table of contents / content /
page-local table of contents), a dark-mode toggle with
``prefers-color-scheme`` detection, code-copy buttons, and mobile-friendly
responsive design via an off-canvas navigation drawer.

Features
========

* **Bootstrap 5** — no jQuery dependency.
* **Three-column layout** — global site TOC on the left, local page TOC on
  the right, collapsing gracefully on smaller viewports.
* **Dark mode** — follows the OS preference automatically; a toggle button
  lets users override it.  The preference is persisted in ``localStorage``.
* **Code copy buttons** — every code block gets a one-click copy button.
* **Off-canvas mobile TOC** — the full site TOC is accessible on mobile via
  a "Contents" button in the navbar.
* **Accessibility** — skip-navigation link, ARIA labels, correct DOM order.
* **Steps extension** — ``kentigern.ext.steps`` provides a ``steps``
  directive for numbered step-by-step procedures.
* **Webpack build pipeline** — all CSS and JS are compiled from SCSS/ES
  source and bundled with webpack.

Installation
============

Install from PyPI_::

    pip install kentigern

Then add to your Sphinx ``conf.py``::

    extensions = [
        # optional — add the steps directive
        "kentigern.ext.steps",
    ]

    html_theme = "kentigern"

Configuration
=============

Kentigern supports the following ``html_theme_options`` keys:

``navbar_title``
    Brand title shown in the navbar.  Defaults to the project name.

``navbar_links``
    List of extra links to add to the navbar, as a list of
    ``(title, url, external)`` triples.

``globaltoc_depth``
    Maximum depth to render in the global site TOC.  Defaults to ``-1``
    (unlimited).

Changelog
=========

See `HISTORY.rst <HISTORY.rst>`_ for the full version history.

Licence
=======

Kentigern is released under the `MIT licence`_.

.. _Sphinx: https://www.sphinx-doc.org/
.. _Bootstrap 5: https://getbootstrap.com/
.. _PyPI: https://pypi.org/project/kentigern/
.. _MIT licence: LICENSE.txt
