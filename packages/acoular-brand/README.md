# acoular-brand

Shared visual design assets for the Acoular organization.

`src/acoular_brand/theme.toml` is the single editable colour source. Rendered
CSS, Matplotlib, and Bokeh assets are committed so consumers need no build step.

```bash
uv run python packages/acoular-brand/tools/build_assets.py
uv run python packages/acoular-brand/tools/build_assets.py --check
```

Consumers can resolve files with `importlib.resources.files("acoular_brand.assets")`.
Use `acoular.css` for named `--acoular-color-*` CSS variables and
`acoular.mplstyle` with `matplotlib.style.use`. `acoular-sphinx` provides
`pydata.css`, which imports `acoular.css` and configures PyData Sphinx Theme.
