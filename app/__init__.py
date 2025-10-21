from __future__ import annotations

import os

# Enable the new experimental OpenAPI parser for FastMCP
# This must be set before importing FastMCP to ensure tools are properly created
os.environ["FASTMCP_EXPERIMENTAL_ENABLE_NEW_OPENAPI_PARSER"] = "true"

from .main import app, create_app, mcp

__all__ = ["app", "create_app", "mcp"]
