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

1. Clone the repository:

```bash
cd marketfiyati_mcp
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Server

Start the server using uvicorn:

```bash
uvicorn app.main:app --reload --port 8000
```

The server will be available at:

- API Documentation: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>
- MCP Endpoint: <http://localhost:8000/mcp>

### API Endpoints

#### 1. Search Products by Categories (POST)

```bash
curl -X POST "http://localhost:8000/search_by_categories" \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": "Meyve ve Sebze",
    "latitude": 39.9366619061509,
    "longitude": 32.5859851407316,
    "pages": 0,
    "size": 24,
    "menuCategory": true,
    "distance": 5,
    "depots": ["bim-U751", "a101-G013", "migros-7845"]
  }'
```

#### 2. Search Products by Categories (GET)

```bash
curl "http://localhost:8000/search_by_categories?keywords=Meyve%20ve%20Sebze&latitude=39.9366&longitude=32.5859&pages=0&size=24"
```

#### 3. Health Check

```bash
curl "http://localhost:8000/health"
```

### Request Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| keywords | string | Yes | - | Search keywords or category name |
| latitude | float | Yes | - | User latitude coordinate |
| longitude | float | Yes | - | User longitude coordinate |
| pages | integer | No | 0 | Page number for pagination |
| size | integer | No | 24 | Number of results per page (1-100) |
| menuCategory | boolean | No | true | Search in menu categories |
| distance | integer | No | 5 | Search radius in kilometers |
| depots | array | No | null | List of depot IDs to search in |

### Response Structure

```json
{
  "numberOfFound": 123,
  "searchResultType": 1,
  "content": [
    {
      "id": "0000000000X3B",
      "title": "Pembe Domates",
      "brand": "Markasız",
      "imageUrl": "https://cdn.marketfiyati.org.tr/...",
      "refinedQuantityUnit": null,
      "refinedVolumeOrWeight": "1 kg",
      "categories": ["Meyve ve Sebze", "Sebze"],
      "productDepotInfoList": [
        {
          "depotId": "bim-D216",
          "depotName": "Muammer Aksoy  Sincan",
          "price": 59.0,
          "unitPrice": "59,00 ₺/kg",
          "marketAdi": "bim",
          "percentage": 0.0,
          "longitude": 32.58121,
          "latitude": 39.94765,
          "indexTime": "20.10.2025 11:11"
        }
      ]
    }
  ],
  "facetMap": {
    "sub_category": [
      {"name": "Dondurulmuş Ürünler", "count": 41},
      {"name": "Sebze", "count": 17}
    ],
    "brand": [
      {"name": "Markasız", "count": 60}
    ],
    "market_names": [
      {"name": "a101", "count": 58},
      {"name": "migros", "count": 36}
    ]
  }
}
```

## Using with MCP Clients

### Claude Desktop Configuration

Add to your Claude Desktop config file (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "marketfiyat": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

### Other MCP Clients

The MCP endpoint is available at `/mcp` and follows the standard MCP protocol. Configure your MCP client to use:

```text
http://localhost:8000/mcp
```

## Project Structure

```text
marketfiyati_mcp/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration settings
│   ├── mcp.py              # MCP server configuration
│   ├── lifespan.py         # Lifecycle management
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py       # Main API router
│   │   ├── dependencies.py # Dependency injection
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── health.py   # Health check endpoint
│   │       └── search.py   # Search endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   └── marketfiyat.py  # Data models
│   └── services/
│       ├── __init__.py
│       └── marketfiyat_service.py  # API service
├── requirements.txt
└── README.md
```

## Configuration

Edit `app/config.py` to customize:

- `DEFAULT_CACHE_SECONDS`: Cache duration for API responses (default: 300 seconds)
- `MARKETFIYAT_BASE_URL`: Base URL for the Marketfiyat API
- `ALLOWED_ORIGINS`: CORS allowed origins

## Development

### Setting Up Development Environment

```bash
# Install all dependencies (including dev dependencies)
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=app --cov-report=term-missing

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_health.py
```

### Code Quality

```bash
# Lint and auto-fix issues with ruff
ruff check --fix app/ tests/

# Format code with ruff
ruff format app/ tests/

# Type check with mypy
mypy app/ --ignore-missing-imports

# Run all pre-commit hooks manually
pre-commit run --all-files
```

### Continuous Integration

This project uses GitHub Actions for CI/CD. The workflow includes:

- **Testing**: Runs tests on Python 3.10, 3.11, and 3.12
- **Linting**: Checks code formatting and linting with ruff and mypy
- **Pre-commit**: Validates all pre-commit hooks

The CI pipeline runs automatically on:

- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

## Common Use Cases

### 1. Find Cheapest Tomatoes Near You

```python
import httpx

response = httpx.post("http://localhost:8000/search_by_categories", json={
    "keywords": "domates",
    "latitude": 39.9366,
    "longitude": 32.5859,
    "distance": 5,
    "size": 10
})

products = response.json()["content"]
for product in products:
    print(f"{product['title']}: {product['productDepotInfoList'][0]['price']} TL")
```

### 2. Compare Prices Across Markets

```python
response = httpx.post("http://localhost:8000/search_by_categories", json={
    "keywords": "süt",
    "latitude": 39.9366,
    "longitude": 32.5859,
    "depots": ["bim-D216", "a101-G013", "migros-7845"]
})

# Compare prices for the same product across different markets
```

### 3. Browse by Category

```python
response = httpx.post("http://localhost:8000/search_by_categories", json={
    "keywords": "Meyve ve Sebze",
    "latitude": 39.9366,
    "longitude": 32.5859,
    "menuCategory": True,
    "size": 50
})

# Get all products in the "Fruits and Vegetables" category
```

## License

This project is licensed under the MIT License.

## Acknowledgments

- Data provided by [marketfiyati.org.tr](https://marketfiyati.org.tr)

## Support

For issues and questions, please open an issue on GitHub.
