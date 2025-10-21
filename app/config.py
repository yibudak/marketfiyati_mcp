from __future__ import annotations

from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore


def _get_version() -> str:
    """Read version from pyproject.toml"""
    try:
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        with open(pyproject_path, "rb") as f:
            pyproject_data = tomllib.load(f)
        return pyproject_data["project"]["version"]
    except (FileNotFoundError, KeyError):
        return "1.0.0"  # Fallback version


API_TITLE = "Marketfiyat MCP API"
API_DESCRIPTION = (
    "Marketfiyat MCP API provides access to Turkish market product prices from "
    "marketfiyati.org.tr, allowing you to search products by categories, keywords, "
    "and location, and compare prices across different markets."
)
API_VERSION = _get_version()

MARKETFIYAT_BASE_URL = "https://api.marketfiyati.org.tr"
DEFAULT_CACHE_SECONDS = 300  # 5 minutes cache for price data
ALLOWED_ORIGINS = ["*"]
