from __future__ import annotations

API_TITLE = "Marketfiyat MCP API"
API_DESCRIPTION = (
    "Marketfiyat MCP API provides access to Turkish market product prices from "
    "marketfiyati.org.tr, allowing you to search products by categories, keywords, "
    "and location, and compare prices across different markets."
)
API_VERSION = "1.0.0"

MARKETFIYAT_BASE_URL = "https://api.marketfiyati.org.tr"
DEFAULT_CACHE_SECONDS = 300  # 5 minutes cache for price data
ALLOWED_ORIGINS = ["*"]
