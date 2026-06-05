import warnings
from pathlib import Path

# Path to the ruff configuration file
RUFF_CONFIG = Path(__file__).parent / "ruff.acoular.toml"

warnings.warn('This package does not contain any code; only ruff.acoular.toml.')
