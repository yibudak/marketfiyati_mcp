from __future__ import annotations

from fastapi import FastAPI
from fastmcp import FastMCP

try:  # pragma: no cover - depends on installed FastMCP version
    from fastmcp.experimental.server.openapi import MCPType, RouteMap
except ImportError:  # pragma: no cover
    from fastmcp.server.openapi import MCPType, RouteMap

from .lifespan import merge_lifespans


def configure_mcp(app: FastAPI) -> FastMCP:
    route_maps = [
        RouteMap(
            methods=["GET"],
            pattern=r".*",
            mcp_type=MCPType.TOOL,
        ),
        RouteMap(
            methods=["POST"],
            pattern=r".*",
            mcp_type=MCPType.TOOL,
        ),
        # Other methods fall back to default TOOL mapping
    ]

    mcp_server = FastMCP.from_fastapi(
        app=app,
        name="Marketfiyat MCP",
        route_maps=route_maps,
    )

    mcp_http = mcp_server.http_app(path="/")
    app.mount("/mcp", mcp_http, name="mcp")
    app.router.lifespan_context = merge_lifespans(
        app.router.lifespan_context, mcp_http.lifespan
    )
    app.state.mcp = mcp_server
    app.state.mcp_http = mcp_http

    return mcp_server
