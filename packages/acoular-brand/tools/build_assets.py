#!/usr/bin/env python3
"""Render distributable style assets from ``src/acoular_brand/theme.toml``."""

from __future__ import annotations

import argparse
import tomllib
from pathlib import Path

ROOT = Path(__file__).parents[1]
TOKENS = ROOT / "src" / "acoular_brand" / "theme.toml"
ASSETS = ROOT / "src" / "acoular_brand" / "assets"


def color(tokens: dict, name: str) -> str:
    return tokens["colors"][name]


def render_acoular_css(tokens: dict) -> str:
    variables = "\n".join(
        f"  --acoular-color-{name}: {value};"
        for name, value in tokens["colors"].items()
    )
    return f"""/* Generated from acoular_brand/theme.toml; do not edit. */
:root {{
{variables}
}}
"""



def render_mplstyle(tokens: dict) -> str:
    def mpl_color(name: str) -> str:
        return f'"{color(tokens, name)}"'

    colors = ", ".join(
        f'"{color(tokens, name)}"'
        for name in ("brand", "danger", "success", "warning", "secondary-light", "muted-dark")
    )
    return f"""# Generated from acoular_brand/theme.toml; do not edit.
font.family: sans-serif
font.sans-serif: Roboto, Roboto Condensed, DejaVu Sans, Arial, sans-serif
font.monospace: Source Code Pro, DejaVu Sans Mono, monospace
text.color: {mpl_color("brand")}
text.usetex: True
axes.labelcolor: {mpl_color("brand")}
axes.edgecolor: {mpl_color("brand")}
axes.titlecolor: {mpl_color("brand")}
xtick.color: {mpl_color("brand")}
ytick.color: {mpl_color("brand")}
figure.facecolor: {mpl_color("background-light")}
axes.facecolor: {mpl_color("background-light")}
savefig.facecolor: {mpl_color("background-light")}
grid.color: {mpl_color("muted-dark")}
grid.alpha: 0.25
axes.grid: True
axes.axisbelow: True
axes.prop_cycle: cycler('color', [{colors}])
lines.linewidth: 1.8
"""



def rendered_assets() -> dict[Path, str]:
    with TOKENS.open("rb") as file:
        tokens = tomllib.load(file)
    return {
        ASSETS / "acoular.css": render_acoular_css(tokens),
        ASSETS / "acoular.mplstyle": render_mplstyle(tokens),
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
