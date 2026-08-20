"""Pygments styles derived from the packaged Acoular theme."""

from __future__ import annotations

import tomllib
from importlib.resources import files

from pygments.style import Style
from pygments.token import Comment, Error, Generic, Keyword, Name, Number, Operator, String, Text, Whitespace

with files("acoular_brand").joinpath("theme.toml").open("rb") as _file:
    _THEME = tomllib.load(_file)


def _theme_colors(name: str) -> dict[str, str]:
    return {
        role: _THEME["colors"][color]
        for role, color in _THEME[name].items()
    }


def _styles(colors: dict[str, str]) -> dict:
    return {
        Text: colors["text"],
        Whitespace: "",
        Comment: f"italic {colors['muted']}",
        Error: colors["danger"],
        Keyword: colors["danger"],
        Name: colors["text"],
        Name.Builtin: colors["accent"],
        Name.Class: f"bold {colors['brand']}",
        Name.Function: colors["brand"],
        Number: colors["warning"],
        Operator: colors["accent"],
        String: colors["hover"],
        Generic.Heading: f"bold {colors['brand']}",
        Generic.Error: colors["danger"],
        Generic.Prompt: colors["muted"],
    }


class AcoularLightStyle(Style):
    """Acoular palette on the light documentation background."""

    colors = _theme_colors("light")
    background_color = colors["surface"]
    default_style = ""
    styles = _styles(colors)


class AcoularDarkStyle(Style):
    """Acoular palette on the dark documentation background."""

    colors = _theme_colors("dark")
    background_color = colors["surface"]
    default_style = ""
    styles = _styles(colors)
