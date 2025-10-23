# Marketfiyati MCP Server

A Model Context Protocol (MCP) server for accessing Turkish market product prices from [marketfiyati.org.tr](https://marketfiyati.org.tr). This server provides a standardized API for searching products across different Turkish supermarket chains (BIM, A101, Migros, SOK, etc.) and comparing prices.

## Disclaimer

This is an **educational project** created for learning purposes. It is **not intended for commercial use**. All data is sourced from [marketfiyati.org.tr](https://marketfiyati.org.tr). Please respect their terms of service and use this project responsibly.

## Features

- 🔍 Search products by keywords and categories
- 📍 Location-based search with nearby stores
- 🏪 Multi-market price comparison
- 💰 Price tracking and unit price calculations
- 🚀 Fast response with intelligent caching
- 🔌 MCP-compatible for easy integration with AI tools

## Installation

### Using Docker (Recommended)

```bash
# Pull the pre-built image
docker pull ghcr.io/yibudak/marketfiyati_mcp:latest

# Run the container
docker run -d -p 8000:8000 --name marketfiyati-mcp ghcr.io/yibudak/marketfiyati_mcp:latest

# Run with SOCKS proxy (optional)
docker run -d -p 8000:8000 -e SOCKS_PROXY=socks5://localhost:1080 --name marketfiyati-mcp ghcr.io/yibudak/marketfiyati_mcp:latest
```

The server will be available at <http://localhost:8000>

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/yibudak/marketfiyati_mcp.git
cd marketfiyati_mcp

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --port 8000

# Run with SOCKS proxy (optional)
SOCKS_PROXY=socks5://localhost:1080 uvicorn app.main:app --port 8000
```

## API Endpoints

The server provides the following endpoints:

- **POST /search_by_categories** - Search products with detailed filters (keywords, location, depot IDs)
- **GET /search_by_categories** - Simple product search via query parameters
- **GET /health** - Health check endpoint (includes version info)
- **GET /version** - Get API version
- **GET /docs** - Interactive API documentation (Swagger UI)
- **GET /mcp** - MCP protocol endpoint for AI tool integration

For detailed API documentation, visit <http://localhost:8000/docs> after starting the server.

## SOCKS Proxy Configuration

The server supports SOCKS proxy for all external API calls to marketfiyati.org.tr. This is useful when you need to route requests through a proxy server.

### Supported Proxy Types

- SOCKS5 (recommended): `socks5://host:port`
- SOCKS5 with authentication: `socks5://username:password@host:port`
- SOCKS4: `socks4://host:port`

### Configuration Methods

#### Environment Variable

Set the `SOCKS_PROXY` environment variable before starting the server:

```bash
# Linux/macOS
export SOCKS_PROXY=socks5://localhost:1080
uvicorn app.main:app --port 8000

# Windows (PowerShell)
$env:SOCKS_PROXY="socks5://localhost:1080"
uvicorn app.main:app --port 8000

# Windows (Command Prompt)
set SOCKS_PROXY=socks5://localhost:1080
uvicorn app.main:app --port 8000
```

#### Docker

Pass the proxy configuration as an environment variable:

```bash
docker run -d -p 8000:8000 \
  -e SOCKS_PROXY=socks5://localhost:1080 \
  --name marketfiyati-mcp \
  ghcr.io/yibudak/marketfiyati_mcp:latest
```

### Example Proxy Configurations

```bash
# Local SOCKS5 proxy (e.g., SSH tunnel)
SOCKS_PROXY=socks5://localhost:1080

# Remote SOCKS5 proxy with authentication
SOCKS_PROXY=socks5://myuser:mypass@proxy.example.com:1080

# SOCKS4 proxy
SOCKS_PROXY=socks4://proxy.example.com:1080
```

### Creating a SOCKS Proxy with SSH

You can create a local SOCKS5 proxy using SSH:

```bash
# Create an SSH tunnel that acts as a SOCKS5 proxy on port 1080
ssh -D 1080 -C -N user@remote-server.com

# Then run the server with the proxy
SOCKS_PROXY=socks5://localhost:1080 uvicorn app.main:app --port 8000
```

## Using with Claude Desktop

Add the following configuration to your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "marketfiyati": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

After adding the configuration, restart Claude Desktop. The MCP server will be available for product price searches.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Data provided by [marketfiyati.org.tr](https://marketfiyati.org.tr)

## Support

For issues and questions, please open an issue on [GitHub](https://github.com/yibudak/marketfiyati_mcp/issues).
