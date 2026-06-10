from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

_TEMPLATE_DIR = Path(__file__).parent / "_templates"

_PRIMARY_NAV_LINKS = [
    {"label": "Home", "url": "/", "external": False},
    {"label": "Blog", "url": "https://blog.acoular.org", "external": True},
    {"label": "Community", "url": "https://github.com/orgs/acoular/discussions", "external": True},
    {"label": "Contribute", "url": "/contribute/", "external": False},
]

_PACKAGE_NAV_LINKS = [
    {"label": "Acoular", "url": "/acoular/", "external": False},
    {"label": "SpectAcoular", "url": "/spectacoular/", "external": False},
    {"label": "AcouPipe", "url": "/acoupipe/", "external": False},
]


def build_html_context() -> dict[str, list[dict[str, Any]]]:
    return {
        "acoular_nav_links": deepcopy(_PRIMARY_NAV_LINKS),
        "acoular_package_links": deepcopy(_PACKAGE_NAV_LINKS),
    }



def configure_theme_options(
    *,
    use_edit_page_button: bool = False,
    show_toc_level: int = 1,
    switcher_json_url: str | None = None,
    version_match: str | None = None,
) -> dict[str, Any]:
    options: dict[str, Any] = {
        "show_toc_level": show_toc_level,
        "header_links_before_dropdown": 4,
        "header_dropdown_text": "Packages",
        "use_edit_page_button": use_edit_page_button,
        "navbar_center": ["acoular-orga-navbar"],
    }
    if switcher_json_url and version_match:
        options["switcher"] = {
            "json_url": switcher_json_url,
            "version_match": version_match,
        }
        options["show_version_warning_banner"] = True
        options["navbar_center"].append("version-switcher")
    return options



def _on_config_inited(app, config) -> None:
    template_path = str(_TEMPLATE_DIR)
    if template_path not in config.templates_path:
        config.templates_path.append(template_path)



def setup(app):
    app.connect("config-inited", _on_config_inited)
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


__all__ = ["build_html_context", "configure_theme_options"]
