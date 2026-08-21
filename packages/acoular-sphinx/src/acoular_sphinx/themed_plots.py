"""Sphinx-Gallery scraper for light and dark Matplotlib plot assets."""

import os
from pathlib import Path

_DARK_FOREGROUND = "#f5f9ff"
_DARK_GRID = "#626a7c"
_DARK_LINE_COLORS = {
    "#000000": _DARK_FOREGROUND,
    "#0c3762": "#fbf4d7",  # brand
    "#005b46": "#3cc5d0",  # success
    "#5e2132": "#ffa1d7",  # secondary-dark
    "#626a7c": "#b6bdce",  # muted-dark
}


def _set_text_color(text, color):
    if text is not None:
        text.set_color(color)


def apply_dark_theme(figure):
    """Restyle an existing Matplotlib figure for the dark documentation theme."""
    from matplotlib.text import Text

    for text in figure.findobj(Text):
        _set_text_color(text, _DARK_FOREGROUND)

    for axes in figure.axes:
        axes.tick_params(colors=_DARK_FOREGROUND)
        for line in axes.get_lines():
            if color := _dark_line_color(line.get_color()):
                line.set_color(color)
        if not hasattr(axes, "_colorbar"):
            for mappable in (*axes.images, *axes.collections):
                mappable.set_cmap("acoular")
        for spine in axes.spines.values():
            spine.set_color(_DARK_FOREGROUND)
        for line in axes.get_xgridlines() + axes.get_ygridlines():
            line.set_color(_DARK_GRID)
        if legend := axes.get_legend():
            legend.get_frame().set_alpha(0)
            legend.get_frame().set_edgecolor(_DARK_FOREGROUND)


def _dark_line_color(color):
    """Return a contrast-safe replacement for a light-theme line colour."""
    from matplotlib.colors import to_hex

    try:
        return _DARK_LINE_COLORS.get(to_hex(color))
    except ValueError:
        return None


def _themed_image_rst(image_path, source_dir, alt):
    relative_path = os.path.relpath(image_path, source_dir).replace(os.sep, "/")
    alt = alt.replace("\n", " ")
    dark_path = f"{relative_path.removesuffix(image_path.suffix)}-dark{image_path.suffix}"
    return f""".. container:: acoular-themed-plot acoular-plot-light

   .. image-sg:: /{relative_path}
      :alt: {alt}
      :srcset: /{relative_path}
      :class: sphx-glr-single-img

.. container:: acoular-themed-plot acoular-plot-dark

   .. image-sg:: /{dark_path}
      :alt: {alt}
      :srcset: /{dark_path}
      :class: sphx-glr-single-img

"""


def themed_matplotlib_scraper(block, block_vars, gallery_conf):
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
        figure.savefig(light_path, transparent=True)
        apply_dark_theme(figure)
        dark_path = light_path.with_stem(f"{light_path.stem}-dark")
        figure.savefig(dark_path, transparent=True)
        images_rst.append(
            _themed_image_rst(light_path, gallery_conf["src_dir"], _matplotlib_fig_titles(figure))
        )

    plt.close("all")
    return "".join(images_rst)


def _configure_sphinx_gallery(_app, config):
    if config.acoular_sphinx_themed_plots:
        config.sphinx_gallery_conf["image_scrapers"] = (themed_matplotlib_scraper,)


def setup(app):
    """Register themed plot scraping after Sphinx-Gallery is configured."""
    app.add_css_file("sphinx_gallery.css")
    app.connect("config-inited", _configure_sphinx_gallery, priority=1000)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
