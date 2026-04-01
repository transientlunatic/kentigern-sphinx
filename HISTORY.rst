=========
 History
=========

v0.5.0
======
* Add steps directive and extension (``kentigern.ext.steps``).
* Fix stale ``storedTheme`` check in ``darkmode.js``.
* Accessibility: add visually-hidden skip-navigation link.
* Accessibility: add ``aria-label`` to dark-mode toggle button.
* Accessibility: fix Bootstrap 4 ``data-toggle``/``data-target`` attributes
  to Bootstrap 5 equivalents — mobile nav now works correctly.
* Accessibility: fix DOM column order to match visual order; remove all
  ``order-*`` classes.
* Responsive: rationalise three-column grid breakpoints (``<lg`` full-width,
  ``lg`` two-column, ``xl+`` three-column).
* Responsive: mobile global TOC via Bootstrap 5 Offcanvas drawer.
* Responsive: sticky local TOC now activates at ``lg+`` (992 px).
* Build: fix ``basics.scss`` not being imported — critical bug that caused
  all global styles to be absent from compiled CSS.
* Build: remove duplicate ``bootstrap-icons`` import (~77 KB CSS saving).

v0.4.0
======
* Fix webpack to use ``mini-css-extract-plugin``, producing a real
  ``kentigern-modern.css`` file rather than injecting styles via JS.
* Remove jQuery CDN dependency (Bootstrap 5 does not require it).
* Initialise Bootstrap 5 ScrollSpy via vanilla JS.
* Remove ``maximum-scale=1`` from viewport meta (WCAG 2.1 SC 1.4.4).
* Fix ``basics.scss``: remove legacy ``@import url(...)`` CSS statements
  that caused 404s in the browser.
* Move ``code-copy.js`` into the webpack bundle.
* Tidy source tree: delete pre-compiled artefacts and legacy Bootstrap 3
  jQuery template from ``theme-files/``.
* Update Makefile clean target to remove generated assets.

v0.3.0
======
* Internal cleanup release.

v0.2.0
======
* Migrate from Bootstrap 3 to **Bootstrap 5**.
* New three-column layout: global TOC / content / local TOC.
* Dark-mode toggle with ``prefers-color-scheme`` detection.
* Code copy buttons on all code blocks.
* Webpack-based build pipeline for CSS and JavaScript.

v0.1.8
======
* Sidebar and layout improvements.

v0.1.7
======
* Updated right sidebar styling.

v0.1.6
======
* Updated figure handling.
