"""Pygments styles derived from the packaged Acoular theme."""

from __future__ import annotations

import tomllib
from importlib.resources import files

from pygments.style import Style
from pygments.token import Comment, Error, Generic, Keyword, Name, Number, Operator, String, Text, Whitespace

with files("acoular_brand").joinpath("theme.toml").open("rb") as _file:
    _THEME = tomllib.load(_file)


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

    background_color = _THEME["light"]["surface"]
    default_style = ""
    styles = _styles(_THEME["light"])


class AcoularDarkStyle(Style):
    """Acoular palette on the dark documentation background."""

    background_color = _THEME["dark"]["surface"]
    default_style = ""
    styles = _styles(_THEME["dark"])
