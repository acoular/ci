from __future__ import annotations

import os
from copy import deepcopy
from pathlib import Path
from typing import Any

_PACKAGE_DIR = Path(__file__).parent
_TEMPLATE_DIR = _PACKAGE_DIR / "_templates"
_STATIC_DIR = _PACKAGE_DIR / "_static"

_NAV_LINKS = [
    {"label": "Home", "url": "https://www.acoular.org/", "external": True},
    {"label": "Acoular", "url": "https://www.acoular.org/acoular/", "external": True},
    {
        "label": "SpectAcoular",
        "url": "https://www.acoular.org/spectacoular/",
        "external": True,
    },
    {
        "label": "AcouPipe",
        "url": "https://adku1173.github.io/acoupipe/",
        "external": True,
    },
    {"label": "Blog", "url": "https://blog.acoular.org", "external": True},
    {
        "label": "Community",
        "url": "https://github.com/orgs/acoular/discussions",
        "external": True,
    },
    {
        "label": "Contributing",
        "url": "https://www.acoular.org/contributing/",
        "external": True,
    },
]

COMMON_EXTENSIONS = [
    "acoular_sphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "traits.util.trait_documenter",
]

PACKAGE_FRAME_EXTENSIONS = [
    *COMMON_EXTENSIONS,
    "IPython.sphinxext.ipython_console_highlighting",
    "IPython.sphinxext.ipython_directive",
    "matplotlib.sphinxext.plot_directive",
    "numpydoc",
    "sphinx.ext.duration",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.mathjax",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_gallery.gen_gallery",
    "sphinxcontrib.bibtex",
]


def build_html_context() -> dict[str, list[dict[str, Any]]]:
    return {
        "acoular_nav_links": deepcopy(_NAV_LINKS),
    }


def build_github_context(
    *,
    github_user: str,
    github_repo: str,
    doc_path: str,
    github_version: str = "master",
) -> dict[str, str]:
    return {
        "github_user": github_user,
        "github_repo": github_repo,
        "github_version": github_version,
        "doc_path": doc_path,
    }


def shared_static_asset(name: str) -> str:
    return str(_STATIC_DIR / name)


def resolve_docs_build_config(
    *,
    default_version_match: str = "",
    default_switcher_json_url: str = "_static/switcher.json",
) -> dict[str, str]:
    return {
        "html_baseurl": os.environ.get("DOCS_BASEURL", ""),
        "version_match": os.environ.get("DOCS_VERSION_MATCH", default_version_match),
        "switcher_json_url": os.environ.get(
            "DOCS_SWITCHER_JSON_URL",
            default_switcher_json_url,
        ),
    }


def configure_theme_options(
    *,
    use_edit_page_button: bool = False,
    show_toc_level: int = 1,
    switcher_json_url: str | None = None,
    version_match: str | None = None,
) -> dict[str, Any]:
    options: dict[str, Any] = {
        "logo": {
            "alt_text": "Acoular",
            "text": "Acoular Organization",
            "image_light": "_static/acoular_logo_light.png",
            "image_dark": "_static/acoular_logo_dark.png",
        },
        "icon_links": [
            {
                "name": "GitHub",
                "url": "https://github.com/acoular",
                "icon": "fa-brands fa-square-github",
            },
            {
                "name": "PyPI",
                "url": "https://pypi.org/project/acoular",
                "icon": "_static/pypi.svg",
                "type": "local",
            },
        ],
        "pygments_light_style": "tango",
        "pygments_dark_style": "monokai",
        "show_toc_level": show_toc_level,
        "header_links_before_dropdown": 7,
        "header_dropdown_text": "More",
        "use_edit_page_button": use_edit_page_button,
        "navbar_start": ["navbar-logo"],
        "navbar_center": ["acoular-orga-navbar"],
        "collapse_navigation": False,
    }
    if switcher_json_url and version_match:
        options["switcher"] = {
            "json_url": switcher_json_url,
            "version_match": version_match,
        }
        options["show_version_warning_banner"] = True
        options["navbar_start"].append("version-switcher")
    return options


def configure_package_theme_options(
    *,
    package_name: str,
    github_url: str,
    pypi_project: str,
    use_edit_page_button: bool = False,
    show_toc_level: int = 1,
    switcher_json_url: str | None = None,
    version_match: str | None = None,
) -> dict[str, Any]:
    options = configure_theme_options(
        use_edit_page_button=use_edit_page_button,
        show_toc_level=show_toc_level,
        switcher_json_url=switcher_json_url,
        version_match=version_match,
    )
    options.update(
        {
            "logo": {
                "alt_text": f"{package_name} - Home",
                "text": package_name,
                "image_light": "_static/acoular_logo_light.png",
                "image_dark": "_static/acoular_logo_dark.png",
            },
            "icon_links": [
                {
                    "name": "GitHub",
                    "url": github_url,
                    "icon": "fa-brands fa-square-github",
                },
                {
                    "name": "PyPI",
                    "url": f"https://pypi.org/project/{pypi_project}",
                    "icon": "_static/pypi.svg",
                    "type": "local",
                },
            ],
        }
    )
    return options


def _on_config_inited(app, config) -> None:
    template_path = str(_TEMPLATE_DIR)
    if template_path not in config.templates_path:
        config.templates_path.append(template_path)

    static_path = str(_STATIC_DIR)
    if static_path not in config.html_static_path:
        config.html_static_path.append(static_path)

    if not config.html_favicon:
        config.html_favicon = shared_static_asset("acoular_favicon.ico")


def setup(app):
    app.connect("config-inited", _on_config_inited)
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


__all__ = [
    "COMMON_EXTENSIONS",
    "PACKAGE_FRAME_EXTENSIONS",
    "build_github_context",
    "build_html_context",
    "configure_package_theme_options",
    "configure_theme_options",
    "resolve_docs_build_config",
    "shared_static_asset",
]
