# acoular-brand

Shared visual design assets for the Acoular organization.

`src/acoular_brand/theme.toml` is the single editable colour source. Rendered
CSS, Matplotlib, and Bokeh assets are committed so consumers need no build step.

```bash
uv run python packages/acoular-brand/tools/build_assets.py
uv run python packages/acoular-brand/tools/build_assets.py --check
```

Consumers can resolve files with `importlib.resources.files("acoular_brand.assets")`.
Use `acoular.css` for PyData Sphinx Theme and application chrome,
`acoular.mplstyle` with `matplotlib.style.use`, and `acoular.bokeh.json` through
Bokeh's `Theme`.
