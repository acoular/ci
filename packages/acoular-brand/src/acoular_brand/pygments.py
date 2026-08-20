"""Pygments styles derived from the packaged Acoular theme."""

from __future__ import annotations

import tomllib
from importlib.resources import files

from pygments.style import Style
from pygments.token import Comment, Error, Generic, Keyword, Name, Number, Operator, String, Text, Whitespace

with files("acoular_brand").joinpath("theme.toml").open("rb") as _file:
    _THEME = tomllib.load(_file)


def _theme_colors(**roles: str) -> dict[str, str]:
    return {
        role: _THEME["colors"][color]
        for role, color in roles.items()
    }


_LIGHT = _theme_colors(
    surface="background-light",
    text="background-dark",
    muted="muted",
    danger="danger",
    secondary="secondary-dark",
    success="success",
    brand="brand",
    warning="warning",
    accent="accent",
    highlight="highlight",
)
_DARK = _theme_colors(
    surface="background-dark",
    text="muted-light",
    muted="muted-dark",
    danger="danger",
    secondary="secondary-light",
    success="success",
    brand="brand-light",
    warning="warning",
    accent="accent",
    highlight="highlight",
)


def _styles(colors: dict[str, str]) -> dict:
    return {
        Text: colors["text"],
        Whitespace: "",
        Comment: f"italic {colors['muted']}",
        Comment.Preproc: colors["secondary"],
        Error: colors["danger"],
        Keyword: colors["danger"],
        Keyword.Type: colors["secondary"],
        Name: colors["text"],
        Name.Builtin: colors["success"],
        Name.Class: f"bold {colors['brand']}",
        Name.Decorator: colors["accent"],
        Name.Function: colors["brand"],
        Name.Namespace: colors["secondary"],
        Number: colors["warning"],
        Operator: colors["accent"],
        String: colors["highlight"],
        String.Escape: colors["secondary"],
        Generic.Heading: f"bold {colors['brand']}",
        Generic.Subheading: colors["secondary"],
        Generic.Error: colors["danger"],
        Generic.Prompt: colors["muted"],
    }


class AcoularLightStyle(Style):
    """Acoular palette on the light documentation background."""

    colors = _LIGHT
    background_color = colors["surface"]
    default_style = ""
    styles = _styles(colors)


class AcoularDarkStyle(Style):
    """Acoular palette on the dark documentation background."""

    colors = _DARK
    background_color = colors["surface"]
    default_style = ""
    styles = _styles(colors)
