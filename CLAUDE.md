# kentigern-sphinx — Project Notes for Claude

## What this is

A custom Sphinx HTML theme. It wraps Bootstrap 5 and provides a three-column
layout (global TOC / content / local TOC), a dark-mode toggle, code copy
buttons, and custom typography. It is distributed as a Python package and
registered with Sphinx via the `sphinx.html_themes` entry point.

---

## Build System

**All CSS and JavaScript must be authored and built through webpack.**
Do not hand-edit anything under `kentigern/static/` — that directory is the
output of `make css` and will be overwritten.

### Directories

| Path | Purpose |
|---|---|
| `theme-files/src/scss/` | SCSS source files — edit these |
| `theme-files/src/js/` | JS source files — edit these |
| `theme-files/webpack.config.js` | Webpack configuration |
| `theme-files/package.json` | Node dependencies |
| `theme-files/dist/` | Webpack output (intermediate, copied to static) |
| `kentigern/static/` | Final static assets served by Sphinx — **generated, do not edit** |

### Build commands

```bash
make css          # run webpack and copy outputs to kentigern/static
make demo         # build demo docs (runs css first)
make demo_server  # build and serve demo on port 8000
make clean        # remove build artefacts
```

### SCSS entry point

`theme-files/src/scss/styles.scss` imports everything else. Add new component
files there. Variable overrides belong in `variables.scss` (imported first).

---

## Honest Appraisal & Known Issues

### Critical — structural problems that need fixing

1. **Webpack uses `style-loader`, not `mini-css-extract-plugin`.**
   `style-loader` injects CSS into the DOM via JavaScript at runtime — it does
   not write a `.css` file. But `theme.conf` declares `stylesheet =
   kentigern-modern.css`, which means Sphinx expects a separate CSS file.
   The `kentigern-modern.css` currently in `kentigern/static/` is a hand-copied
   pre-compiled artefact, not a real webpack output. This is architecturally
   broken. **Fix:** switch to `mini-css-extract-plugin` so webpack actually
   produces `kentigern-modern.css`.

2. **jQuery is loaded via CDN even though Bootstrap 5 does not need it.**
   `layout.html` loads jQuery 3.7.1 from Google CDN (line 14). The only usage
   is the inline scrollspy bootstrap call in the footer. Bootstrap 5 scrollspy
   is initialised differently (via `bootstrap.ScrollSpy`), so the inline script
   is also broken. jQuery should be removed and the scrollspy initialised
   correctly.

3. **`data-spy="scroll"` / `data-target="#localtoc"` on `<body>` are Bootstrap
   3/4 attributes.** They do nothing in Bootstrap 5. Scrollspy must be
   initialised via JavaScript.

4. **`basics.scss` has legacy CSS `@import url("./basic.css")` statements at
   the top** (lines 12–19) that reference CSS files which do not exist in the
   SCSS source tree. These pass through as literal CSS imports and will produce
   404s in the browser. The file is largely a verbatim copy of the old
   `bootstrap-sphinx.css` and needs a proper SCSS refactor.

### Accessibility — WCAG violations

5. **`maximum-scale=1` in the viewport meta tag** prevents users from zooming.
   This is a WCAG 2.1 SC 1.4.4 (Resize Text) failure. Remove it.

6. **No skip-navigation link.** Screen reader and keyboard users must tab
   through the full navbar before reaching content.

7. **DOM order differs from visual order.** On medium screens the right sidebar
   (`order-2`) appears before the main content (`order-1`) in the DOM, then
   Bootstrap's flex order swaps them visually. This confuses screen readers and
   keyboard navigation.

8. **Dark-mode toggle dropdown has no accessible label.** The button that
   opens it shows only an SVG icon without an `aria-label`.

### Tidiness — files that should not exist or are in the wrong place

9. **`theme-files/kentigern-modern.css` and `kentigern-modern.css.map`** are a
   pre-compiled CSS artefact from a previous build sitting inside the source
   directory. They are not part of the webpack source pipeline and should be
   deleted.

10. **`theme-files/bootstrap-sphinx.js_t`** is a legacy Bootstrap 3-era jQuery
    template file. It is not used by anything. Delete it.

11. **`kentigern/static/darkmode.js`** and
    **`kentigern/static/code-copy.js`** are standalone files loaded
    individually in `layout.html`. They should be moved into the webpack
    pipeline (`theme-files/src/js/`) and bundled with everything else, which
    would reduce the number of HTTP requests and allow minification.
    Note: `darkmode.js` *must* execute before first paint (to avoid flash of
    wrong theme). This is currently achieved by loading it as the first script
    in `<head>`. If it is moved into webpack it needs a separate early-loading
    entry point, or must remain a small inline script.

12. **`Makefile` clean target** does not remove font files or
    `kentigern-modern.css` from `kentigern/static/`. It should so that a clean
    build is genuinely clean.

13. **Root-level `package.json` / `package-lock.json`** (untracked) appear to
    be leftovers. All Node config belongs in `theme-files/`.

### Responsiveness — layout concerns

14. **Three-column grid breakpoints are inconsistent.** The layout uses
    `col-md-6` for both sidebars and `col-md-12` for content, with `col-lg-2`
    / `col-lg-8` at larger sizes. On `md` viewports this means the two sidebars
    occupy a full row (6+6=12) but content is full-width below — which is fine
    — but the `order-*` classes were designed for `xl`, causing awkward
    reordering at `md` and `lg`.

15. **Sidebar scroll behaviour** (`position: sticky`, `overflow-y: auto`) only
    activates at `min-width: 1200px`. Below that, the global TOC is hidden
    entirely (`display: none`) with no mobile-friendly alternative (e.g. an
    off-canvas drawer).

---

## Improvement Plan

### Phase 1 — Fix what is broken

- [x] Switch webpack to `mini-css-extract-plugin` to produce `kentigern-modern.css`.
- [x] Remove jQuery CDN link from `layout.html`. Initialise Bootstrap 5 ScrollSpy via vanilla JS.
- [x] Remove `maximum-scale=1` from viewport meta.
- [x] Fix `basics.scss`: remove the legacy CSS `@import url(...)` lines.

### Phase 2 — Tidy up

- [x] Delete `theme-files/kentigern-modern.css` and `kentigern-modern.css.map`.
- [x] Delete `theme-files/bootstrap-sphinx.js_t`.
- [x] Move `code-copy.js` into `theme-files/src/js/` and import from `main.js`.
- [x] `darkmode.js` strategy: kept as a standalone early-loading script in
      `<head>` (must run before first paint to prevent flash of wrong theme).
      Canonical source is `theme-files/darkmode.js`; `make css` copies it to
      `kentigern/static/`.
- [x] Update `Makefile` clean target to remove font files and CSS from
      `kentigern/static/`.
- [x] Remove root-level `package.json` / `package-lock.json`.

### Phase 3 — Accessibility

- [x] Add a visually hidden skip-navigation link as the first focusable element.
      Links to `#main-content`. Appears centred at top of viewport on focus.
- [x] Add `aria-label="Toggle colour theme"` to the dark-mode toggle button.
- [x] Fix DOM order of three-column layout. Columns are now global-toc → content
      → local-toc in the DOM, matching visual order at all breakpoints. All
      `order-*` classes removed.
- [x] Fix Bootstrap 4 navbar toggler attributes (`data-toggle`, `data-target`)
      → Bootstrap 5 (`data-bs-toggle`, `data-bs-target`). Mobile nav now works.
- [ ] Audit dark-mode colour contrast (both light and dark themes) against
      WCAG AA (4.5:1 for normal text, 3:1 for large text). Note: link colour
      `#28a745` in `basics.scss` does not use the `$kentigern-primary` variable
      — this inconsistency should be resolved as part of the contrast audit.
- [ ] Verify all interactive elements are keyboard accessible.

### Phase 4 — Responsive improvements

- [x] Fix `basics.scss` not being imported in `styles.scss` — critical bug
      discovered during Phase 4. All global styles (including Phase 3 skip-nav)
      were absent from the compiled CSS. Also removed a duplicate
      `bootstrap-icons` import (saved ~77 KB from the CSS bundle).
- [x] Rationalise grid breakpoints. New layout:
      `<lg` → content full-width; `lg` → content (9) + local TOC (2); `xl+` → full three columns.
      Column classes: `toc-left: d-none d-xl-block col-xl-2`,
      `content: col-12 col-lg-9 col-xl-8`, `toc-right: d-none d-lg-block col-lg-3 col-xl-2`.
- [x] Mobile global TOC via Bootstrap 5 Offcanvas. A "Contents" button appears
      in the navbar at `<xl` and opens a slide-in panel with the full site TOC.
- [x] Local TOC sticky behaviour activated at `lg+` (992 px) rather than
      `xl+` (1200 px) to match the new breakpoints.
- [ ] Test at common viewport widths: 375, 768, 1024, 1280, 1440.

---

## Colour palette

Defined in `theme-files/src/scss/variables.scss`:

| Variable | Value | Use |
|---|---|---|
| `$kentigern-primary` | `#26934F` (green) | Links, active nav items |
| `$kentigern-secondary` | `#942C26` (red) | Emphasis, code block border |
| `$kentigern-navbar` | same as primary | Navbar background |
| Dark primary | `#BE81F0` (purple) | Dark-mode links |

---

## Python package

- Package name: `kentigern`
- Version: `0.4.1` (defined in both `kentigern/__init__.py` and `setup.py`)
- Sphinx registers the theme via the `sphinx.html_themes` entry point in
  `setup.py`.
- `kentigern/__init__.py` monkeypatches `StandaloneHTMLBuilder` to expose
  navigation objects (`get_nav_object`, `get_page_toc_object`) to Jinja
  templates.

---

## Files to never edit manually

- `kentigern/static/kentigern.js` — webpack output
- `kentigern/static/kentigern-modern.css` — webpack output (once Phase 1 is done)
- `kentigern/static/*.woff`, `*.woff2` — webpack asset outputs
