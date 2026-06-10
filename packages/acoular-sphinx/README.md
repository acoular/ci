# acoular-sphinx

Shared Sphinx helpers for the Acoular organization website and package documentation.

## Features

### Persistent Sidebar for Package Docs

By default, `pydata-sphinx-theme` hides the primary sidebar on index pages. For package documentation where you want the full table of contents permanently visible on the left, use the provided `sidebar-nav-bs.html` template.

**Enable in your package's `docs/conf.py`:**

```python
html_sidebars = {
    "**": ["sidebar-nav-bs.html"],
}
```

This ensures the package TOC is visible on all pages, including the landing page.

**Note:** The theme automatically sets `collapse_navigation: False` to keep the sidebar expanded.

### Shared Templates & Helpers

- `acoular-orga-navbar.html`: Organization navigation bar component
- `build_html_context()`: Shared context for navigation links
- `configure_theme_options()`: Unified theme configuration
- `configure_package_theme_options()`: Package-specific theme setup
