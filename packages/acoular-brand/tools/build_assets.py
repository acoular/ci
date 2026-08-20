#!/usr/bin/env python3
"""Render distributable style assets from ``src/acoular_brand/theme.toml``."""

from __future__ import annotations

import argparse
import json
import tomllib
from pathlib import Path

ROOT = Path(__file__).parents[1]
TOKENS = ROOT / "src" / "acoular_brand" / "theme.toml"
ASSETS = ROOT / "src" / "acoular_brand" / "assets"


def render_css(tokens: dict) -> str:
    def variables(name: str) -> str:
        palette = tokens[name]
        return "\n".join(
            f"  --ac-color-{key}: {value};" for key, value in palette.items()
        )

    return f"""/* Generated from acoular_brand/theme.toml; do not edit. */
:root,
html[data-theme=\"light\"] {{
{variables("light")}
  --pst-color-primary: var(--ac-color-brand);
  --pst-color-secondary: var(--ac-color-accent);
  --pst-color-link: var(--ac-color-brand);
  --pst-color-link-hover: var(--ac-color-accent);
}}

html[data-theme=\"dark\"] {{
{variables("dark")}
  --pst-color-primary: var(--ac-color-brand);
  --pst-color-secondary: var(--ac-color-accent);
  --pst-color-link: var(--ac-color-brand);
  --pst-color-link-hover: var(--ac-color-accent);
}}
"""


def render_mplstyle(tokens: dict) -> str:
    light = tokens["light"]
    colors = ", ".join(repr(color) for color in tokens["plot"]["colors"])
    return f"""# Generated from acoular_brand/theme.toml; do not edit.
figure.facecolor: {light["background"]}
axes.facecolor: {light["background"]}
axes.edgecolor: {light["border"]}
axes.labelcolor: {light["text"]}
axes.titlecolor: {light["text"]}
text.color: {light["text"]}
xtick.color: {light["muted"]}
ytick.color: {light["muted"]}
grid.color: {light["border"]}
grid.alpha: 0.7
axes.grid: True
axes.prop_cycle: cycler('color', [{colors}])
lines.linewidth: 1.8
figure.constrained_layout.use: True
"""


def render_bokeh_theme(tokens: dict) -> str:
    light = tokens["light"]
    return json.dumps(
        {
            "attrs": {
                "Figure": {
                    "background_fill_color": light["background"],
                    "border_fill_color": light["background"],
                    "outline_line_color": light["border"],
                },
                "Axis": {
                    "axis_line_color": light["border"],
                    "major_label_text_color": light["muted"],
                    "axis_label_text_color": light["text"],
                },
                "Grid": {"grid_line_color": light["border"], "grid_line_alpha": 0.7},
                "Title": {"text_color": light["text"]},
            }
        },
        indent=2,
    ) + "\n"


def rendered_assets() -> dict[Path, str]:
    with TOKENS.open("rb") as file:
        tokens = tomllib.load(file)
    return {
        ASSETS / "acoular.css": render_css(tokens),
        ASSETS / "acoular.mplstyle": render_mplstyle(tokens),
        ASSETS / "acoular.bokeh.json": render_bokeh_theme(tokens),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if assets are stale")
    args = parser.parse_args()
    assets = rendered_assets()

    stale = [path for path, content in assets.items() if not path.is_file() or path.read_text() != content]
    if args.check:
        if stale:
            print("Stale generated assets:\n" + "\n".join(str(path.relative_to(ROOT)) for path in stale))
            return 1
        return 0

    for path, content in assets.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
