"""Matplotlib colormaps from the Acoular palette."""

import tomllib
from importlib.resources import files


def register_colormaps():
    """Register the ``acoular`` colormap and its ``acoular_r`` inverse."""
    from matplotlib import colormaps
    from matplotlib.colors import LinearSegmentedColormap

    if "acoular" in colormaps:
        return
    with files("acoular_brand").joinpath("theme.toml").open("rb") as file:
        theme = tomllib.load(file)
    cmap = LinearSegmentedColormap.from_list(
        "acoular_r", [theme["colors"][name] for name in theme["colormap"]["colors"]]
    )
    colormaps.register(cmap)
    colormaps.register(cmap.reversed(name="acoular"))
