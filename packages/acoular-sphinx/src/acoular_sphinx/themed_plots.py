"""Sphinx-Gallery scraper for light and dark Matplotlib plot assets."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

_DARK_BACKGROUND = "#061525"
_DARK_FOREGROUND = "#b6bdce"
_DARK_GRID = "#626a7c"


def _set_text_color(text: Any, color: str) -> None:
    if text is not None:
        text.set_color(color)


def apply_dark_theme(figure: Any) -> None:
    """Restyle an existing Matplotlib figure for the dark documentation theme."""
    from matplotlib.text import Text

    figure.set_facecolor(_DARK_BACKGROUND)
    figure.set_edgecolor(_DARK_BACKGROUND)
    for text in figure.findobj(Text):
        _set_text_color(text, _DARK_FOREGROUND)

    for axes in figure.axes:
        axes.set_facecolor(_DARK_BACKGROUND)
        axes.tick_params(colors=_DARK_FOREGROUND)
        for spine in axes.spines.values():
            spine.set_color(_DARK_FOREGROUND)
        for line in axes.get_xgridlines() + axes.get_ygridlines():
            line.set_color(_DARK_GRID)
        if legend := axes.get_legend():
            legend.get_frame().set_facecolor(_DARK_BACKGROUND)
            legend.get_frame().set_edgecolor(_DARK_FOREGROUND)


def _themed_image_rst(image_path: Path, source_dir: str, alt: str) -> str:
    relative_path = os.path.relpath(image_path, source_dir).replace(os.sep, "/")
    alt = alt.replace("\n", " ")
    return f""".. container:: acoular-themed-plot

   .. image-sg:: /{relative_path}
      :alt: {alt}
      :srcset: /{relative_path}
      :class: sphx-glr-single-img acoular-plot-light

   .. image-sg:: /{relative_path.removesuffix(image_path.suffix)}-dark{image_path.suffix}
      :alt: {alt}
      :srcset: /{relative_path.removesuffix(image_path.suffix)}-dark{image_path.suffix}
      :class: sphx-glr-single-img acoular-plot-dark

"""


def themed_matplotlib_scraper(block: Any, block_vars: dict[str, Any], gallery_conf: dict[str, Any]) -> str:
    """Save every Gallery Matplotlib figure in light and dark variants.

    Examples run once. Their original figure is saved as the light asset, then
    restyled in place and saved as the dark asset. Animated figures retain
    Sphinx-Gallery's standard handling because a static dark copy is invalid.
    """
    import matplotlib.pyplot as plt
    from matplotlib.animation import Animation
    from sphinx_gallery.scrapers import (  # noqa: PLC0415
        _matplotlib_fig_titles,
        matplotlib_scraper,
    )

    animations = {
        animation._fig
        for animation in block_vars["example_globals"].values()
        if isinstance(animation, Animation)
    }
    if animations:
        return matplotlib_scraper(block, block_vars, gallery_conf)

    image_paths = block_vars["image_path_iterator"]
    images_rst = []
    for figure_number, image_path in zip(plt.get_fignums(), image_paths, strict=False):
        light_path = Path(image_path)
        figure = plt.figure(figure_number)
        figure.savefig(light_path)
        apply_dark_theme(figure)
        dark_path = light_path.with_stem(f"{light_path.stem}-dark")
        figure.savefig(dark_path)
        images_rst.append(
            _themed_image_rst(light_path, gallery_conf["src_dir"], _matplotlib_fig_titles(figure))
        )

    plt.close("all")
    return "".join(images_rst)


def _configure_sphinx_gallery(_app: Any, config: Any) -> None:
    if config.acoular_sphinx_themed_plots:
        config.sphinx_gallery_conf["image_scrapers"] = (themed_matplotlib_scraper,)


def setup(app: Any) -> dict[str, bool]:
    """Register themed plot scraping after Sphinx-Gallery is configured."""
    app.connect("config-inited", _configure_sphinx_gallery, priority=1000)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
