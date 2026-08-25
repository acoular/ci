import os
from shutil import which
from copy import deepcopy
from pathlib import Path

from .themed_plots import themed_matplotlib_scraper

from acoular_brand import assets as brand_assets
from acoular_brand.colormaps import register_colormaps
from sphinx_gallery.sorting import ExplicitOrder

_PACKAGE_DIR = Path(__file__).parent
_TEMPLATE_DIR = _PACKAGE_DIR / "_templates"
_STATIC_DIR = _PACKAGE_DIR / "_static"
_BRAND_STATIC_DIR = Path(brand_assets.__file__).parent

_NAV_LINKS = [
    {"label": "Home", "url": "/", "external": False},
    {"label": "Acoular", "url": "/acoular/", "external": False},
    {"label": "SpectAcoular", "url": "/spectacoular/", "external": False},
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
    {"label": "Contributing", "url": "/contributing/", "external": False},
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
    "acoular_sphinx.themed_plots",
    "sphinxcontrib.bibtex",
]


def apply_acoular_mplstyle(_gallery_conf, _fname, when):
    """Apply Acoular's Matplotlib style while Sphinx-Gallery runs an example."""
    if when == "before":
        import matplotlib.style

        register_colormaps()
        matplotlib.style.use(str(_BRAND_STATIC_DIR / "acoular.mplstyle"))
        matplotlib.rcParams["text.usetex"] = which("latex") is not None


def configure_sphinx_gallery(
    *,
    examples_dirs,
    subsection_order=(),
    default_thumb_file=None,
    thumbnail_size=None,
    run_stale_examples=False,
    reset_modules=(),
):
    """Return the shared Sphinx-Gallery configuration for Acoular projects."""
    gallery_conf = {
        "gallery_dirs": "auto_examples",
        "example_extensions": {".py"},
        "filename_pattern": "/example_",
        "reset_modules": (*reset_modules, "matplotlib", "seaborn", apply_acoular_mplstyle),
        "examples_dirs": list(examples_dirs),
    }
    if default_thumb_file:
        gallery_conf["default_thumb_file"] = default_thumb_file
    if thumbnail_size:
        gallery_conf["thumbnail_size"] = thumbnail_size
    if run_stale_examples:
        gallery_conf["run_stale_examples"] = True
    if subsection_order:
        gallery_conf["subsection_order"] = ExplicitOrder(list(subsection_order))
    return gallery_conf


def build_html_context():
    return {
        "acoular_nav_links": deepcopy(_NAV_LINKS),
    }


def build_github_context(
    *,
    github_user,
    github_repo,
    doc_path,
    github_version="master",
):
    return {
        "github_user": github_user,
        "github_repo": github_repo,
        "github_version": github_version,
        "doc_path": doc_path,
    }


def shared_static_asset(name):
    return str(_STATIC_DIR / name)


def resolve_docs_build_config(
    *,
    default_version_match="",
    default_switcher_json_url="_static/switcher.json",
):
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
    use_edit_page_button=False,
    show_toc_level=1,
    switcher_json_url=None,
    version_match=None,
):
    options = {
        "logo": {
            "alt_text": "Acoular",
            "text": "Acoular Organization",
            "image_light": "_static/acoular_logo.svg",
            "image_dark": "_static/acoular_logo_dark_inverted.svg",
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
        "pygments_light_style": "acoular-light",
        "pygments_dark_style": "acoular-dark",
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
    package_name,
    github_url,
    pypi_project,
    use_edit_page_button=False,
    show_toc_level=1,
    switcher_json_url=None,
    version_match=None,
):
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
                "image_light": "_static/acoular_logo.svg",
                "image_dark": "_static/acoular_logo_dark_inverted.svg",
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


def _on_config_inited(app, config):
    import matplotlib

    matplotlib.rcParams["text.usetex"] = which("latex") is not None

    template_path = str(_TEMPLATE_DIR)
    if template_path not in config.templates_path:
        config.templates_path.append(template_path)

    for static_dir in (_STATIC_DIR, _BRAND_STATIC_DIR):
        static_path = str(static_dir)
        if static_path not in config.html_static_path:
            config.html_static_path.append(static_path)

    app.add_css_file("pydata.css")

    if not config.html_favicon:
        config.html_favicon = shared_static_asset("acoular_favicon.ico")



def setup(app):
    app.add_config_value("acoular_sphinx_themed_plots", True, "env", types=[bool])
    app.connect("config-inited", _on_config_inited, priority=1000)
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


__all__ = [
    "COMMON_EXTENSIONS",
    "PACKAGE_FRAME_EXTENSIONS",
    "apply_acoular_mplstyle",
    "build_github_context",
    "build_html_context",
    "configure_package_theme_options",
    "configure_sphinx_gallery",
    "configure_theme_options",
    "resolve_docs_build_config",
    "shared_static_asset",
    "themed_matplotlib_scraper",
]
