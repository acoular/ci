"""Acoular colour tokens."""

import tomllib
from importlib.resources import files

with files("acoular_brand").joinpath("theme.toml").open("rb") as file:
    COLORS = tomllib.load(file)["colors"]
