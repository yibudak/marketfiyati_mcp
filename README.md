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
