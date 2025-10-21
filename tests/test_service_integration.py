"""Integration tests for the MarketfiyatService"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models import (
    DepotLocation,
    NearestDepot,
    SearchByCategoryRequest,
    SearchRequest,
)
from app.services import MarketfiyatService


@pytest.fixture
def service():
    """Create a MarketfiyatService instance"""
    return MarketfiyatService(cache_seconds=0)


@pytest.fixture
def mock_nearest_depots():
    """Mock nearest depots response"""
    return [
        NearestDepot(
            id="bim-U751",
            sellerName="Saraycık Camisincan",
            location=DepotLocation(lon=32.588585, lat=39.941654),
            marketName="bim",
            distance=597.5797281730618,
        ),
        NearestDepot(
            id="a101-G013",
            sellerName="Rahmet Sıncan Ankara",
            location=DepotLocation(lon=32.59425, lat=39.936813),
            marketName="a101",
            distance=704.6070857688579,
        ),
    ]


@pytest.mark.asyncio
async def test_get_nearest_depots(service, mock_nearest_depots):
    """Test getting nearest depots"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "id": "bim-U751",
            "sellerName": "Saraycık Camisincan",
            "location": {"lon": 32.588585, "lat": 39.941654},
            "marketName": "bim",
            "distance": 597.5797281730618,
        },
        {
            "id": "a101-G013",
            "sellerName": "Rahmet Sıncan Ankara",
            "location": {"lon": 32.59425, "lat": 39.936813},
            "marketName": "a101",
            "distance": 704.6070857688579,
        },
    ]

    mock_client = AsyncMock()
    mock_client.post = AsyncMock(return_value=mock_response)

    service._client = mock_client

    result = await service.get_nearest_depots(
        latitude=39.9366619061509, longitude=32.5859851407316, distance=1
    )

    assert len(result) == 2
    assert result[0].id == "bim-U751"
    assert result[0].marketName == "bim"
    assert result[1].id == "a101-G013"
    assert result[1].marketName == "a101"

    # Verify the API was called with correct parameters
    mock_client.post.assert_called_once()
    call_args = mock_client.post.call_args
    assert call_args[0][0] == "/api/v2/nearest"
    assert call_args[1]["json"]["latitude"] == 39.9366619061509
    assert call_args[1]["json"]["longitude"] == 32.5859851407316
    assert call_args[1]["json"]["distance"] == 1


@pytest.mark.asyncio
async def test_search_two_step_process(service):
    """Test that search always uses the two-step process"""
    # Mock nearest depots response
    mock_nearest_response = MagicMock()
    mock_nearest_response.status_code = 200
    mock_nearest_response.json.return_value = [
        {
            "id": "bim-U751",
            "sellerName": "Saraycık Camisincan",
            "location": {"lon": 32.588585, "lat": 39.941654},
            "marketName": "bim",
            "distance": 597.5797281730618,
        },
        {
            "id": "a101-G013",
            "sellerName": "Rahmet Sıncan Ankara",
            "location": {"lon": 32.59425, "lat": 39.936813},
            "marketName": "a101",
            "distance": 704.6070857688579,
        },
    ]

    # Mock search response
    mock_search_response = MagicMock()
    mock_search_response.status_code = 200
    mock_search_response.json.return_value = {
        "numberOfFound": 2,
        "searchResultType": 2,
        "content": [
            {
                "id": "0000000000442",
                "title": "Dost Altın Pastörize Tam Yağlı Süt 1 Lt",
                "brand": "Dost",
                "imageUrl": "https://cdn.marketfiyati.org.tr/bimimages/201013.png",
                "refinedQuantityUnit": None,
                "refinedVolumeOrWeight": "1 lt",
                "categories": ["Süt Ürünleri ve Kahvaltılık", "Süt"],
                "productDepotInfoList": [
                    {
                        "depotId": "bim-U751",
                        "depotName": "Saraycık Camisincan",
                        "price": 38.5,
                        "unitPrice": "38,50 ₺/lt",
                        "marketAdi": "bim",
                        "percentage": 0.0,
                        "longitude": 32.588585,
                        "latitude": 39.941654,
                        "indexTime": "21.10.2025 11:12",
                    }
                ],
            }
        ],
        "facetMap": {
            "sub_category": [{"name": "Tam Yağlı Süt", "count": 1}],
            "refined_quantity_unit": [],
            "main_category": [{"name": "Süt", "count": 2}],
            "refined_volume_weight": [{"name": "1 lt", "count": 1}],
            "brand": [{"name": "Dost", "count": 1}],
            "market_names": [{"name": "bim", "count": 1}],
        },
    }

    mock_client = AsyncMock()

    # Mock post to return different responses based on URL
    async def mock_post(url, **kwargs):
        if url == "/api/v2/nearest":
            return mock_nearest_response
        elif url == "/api/v2/search":
            return mock_search_response
        raise ValueError(f"Unexpected URL: {url}")

    mock_client.post = AsyncMock(side_effect=mock_post)
    service._client = mock_client

    # Create a search request
    request = SearchRequest(
        keywords="tam yağlı süt",
        latitude=39.9366619061509,
        longitude=32.5859851407316,
        pages=0,
        size=24,
        distance=1,
    )

    result = await service.search(request)

    # Verify the result
    assert result.numberOfFound == 2
    assert len(result.content) == 1
    assert result.content[0].title == "Dost Altın Pastörize Tam Yağlı Süt 1 Lt"

    # Verify both API calls were made
    assert mock_client.post.call_count == 2

    # Verify the nearest API was called first
    first_call = mock_client.post.call_args_list[0]
    assert first_call[0][0] == "/api/v2/nearest"

    # Verify the search API was called second with depot IDs
    second_call = mock_client.post.call_args_list[1]
    assert second_call[0][0] == "/api/v2/search"
    search_payload = second_call[1]["json"]
    assert "depots" in search_payload
    assert search_payload["depots"] == ["bim-U751", "a101-G013"]
    assert search_payload["keywords"] == "tam yağlı süt"
    # Verify menuCategory is NOT in the payload
    assert "menuCategory" not in search_payload


@pytest.mark.asyncio
async def test_search_by_categories_two_step_process(service):
    """
    Test that search_by_categories always uses the
    two-step process with menuCategory
    """
    # Mock nearest depots response
    mock_nearest_response = MagicMock()
    mock_nearest_response.status_code = 200
    mock_nearest_response.json.return_value = [
        {
            "id": "bim-U751",
            "sellerName": "Saraycık Camisincan",
            "location": {"lon": 32.588585, "lat": 39.941654},
            "marketName": "bim",
            "distance": 597.5797281730618,
        },
        {
            "id": "a101-G013",
            "sellerName": "Rahmet Sıncan Ankara",
            "location": {"lon": 32.59425, "lat": 39.936813},
            "marketName": "a101",
            "distance": 704.6070857688579,
        },
    ]

    # Mock search response
    mock_search_response = MagicMock()
    mock_search_response.status_code = 200
    mock_search_response.json.return_value = {
        "numberOfFound": 2,
        "searchResultType": 2,
        "content": [
            {
                "id": "0000000000442",
                "title": "Dost Altın Pastörize Tam Yağlı Süt 1 Lt",
                "brand": "Dost",
                "imageUrl": "https://cdn.marketfiyati.org.tr/bimimages/201013.png",
                "refinedQuantityUnit": None,
                "refinedVolumeOrWeight": "1 lt",
                "categories": ["Süt Ürünleri ve Kahvaltılık", "Süt"],
                "productDepotInfoList": [
                    {
                        "depotId": "bim-U751",
                        "depotName": "Saraycık Camisincan",
                        "price": 38.5,
                        "unitPrice": "38,50 ₺/lt",
                        "marketAdi": "bim",
                        "percentage": 0.0,
                        "longitude": 32.588585,
                        "latitude": 39.941654,
                        "indexTime": "21.10.2025 11:12",
                    }
                ],
            }
        ],
        "facetMap": {
            "sub_category": [{"name": "Tam Yağlı Süt", "count": 1}],
            "refined_quantity_unit": [],
            "main_category": [{"name": "Süt", "count": 2}],
            "refined_volume_weight": [{"name": "1 lt", "count": 1}],
            "brand": [{"name": "Dost", "count": 1}],
            "market_names": [{"name": "bim", "count": 1}],
        },
    }

    mock_client = AsyncMock()

    # Mock post to return different responses based on URL
    async def mock_post(url, **kwargs):
        if url == "/api/v2/nearest":
            return mock_nearest_response
        elif url == "/api/v2/search":
            return mock_search_response
        raise ValueError(f"Unexpected URL: {url}")

    mock_client.post = AsyncMock(side_effect=mock_post)
    service._client = mock_client

    # Create a search request with menuCategory
    request = SearchByCategoryRequest(
        keywords="tam yağlı süt",
        latitude=39.9366619061509,
        longitude=32.5859851407316,
        pages=0,
        size=24,
        distance=1,
        menuCategory=True,
    )

    result = await service.search_by_categories(request)

    # Verify the result
    assert result.numberOfFound == 2
    assert len(result.content) == 1
    assert result.content[0].title == "Dost Altın Pastörize Tam Yağlı Süt 1 Lt"

    # Verify both API calls were made
    assert mock_client.post.call_count == 2

    # Verify the nearest API was called first
    first_call = mock_client.post.call_args_list[0]
    assert first_call[0][0] == "/api/v2/nearest"

    # Verify the search API was called second with depot IDs
    second_call = mock_client.post.call_args_list[1]
    assert second_call[0][0] == "/api/v2/search"
    search_payload = second_call[1]["json"]
    assert "depots" in search_payload
    assert search_payload["depots"] == ["bim-U751", "a101-G013"]
    assert search_payload["keywords"] == "tam yağlı süt"
    # Verify menuCategory IS in the payload
    assert "menuCategory" in search_payload
    assert search_payload["menuCategory"] is True


@pytest.mark.asyncio
async def test_get_categories(service):
    """Test getting categories"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "content": [
            {
                "name": "Meyve ve Sebze",
                "subcategories": ["Meyve", "Sebze"],
            },
            {
                "name": "Süt Ürünleri ve Kahvaltılık",
                "subcategories": ["Süt", "Yumurta", "Peynir", "Yoğurt"],
            },
        ]
    }

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    service._client = mock_client

    result = await service.get_categories()

    # Verify the result
    assert len(result.content) == 2
    assert result.content[0].name == "Meyve ve Sebze"
    assert len(result.content[0].subcategories) == 2
    assert result.content[1].name == "Süt Ürünleri ve Kahvaltılık"
    assert len(result.content[1].subcategories) == 4

    # Verify the API was called with correct endpoint
    mock_client.get.assert_called_once_with("/api/v1/info/categories")


@pytest.mark.asyncio
async def test_search_with_different_distances(service):
    """Test that search uses the distance parameter correctly"""
    # Mock nearest depots response
    mock_nearest_response = MagicMock()
    mock_nearest_response.status_code = 200
    mock_nearest_response.json.return_value = [
        {
            "id": "bim-U751",
            "sellerName": "Saraycık Camisincan",
            "location": {"lon": 32.588585, "lat": 39.941654},
            "marketName": "bim",
            "distance": 597.5797281730618,
        },
    ]

    # Mock search response
    mock_search_response = MagicMock()
    mock_search_response.status_code = 200
    mock_search_response.json.return_value = {
        "numberOfFound": 1,
        "searchResultType": 2,
        "content": [],
        "facetMap": {},
    }

    mock_client = AsyncMock()

    # Mock post to return different responses based on URL
    async def mock_post(url, **kwargs):
        if url == "/api/v2/nearest":
            return mock_nearest_response
        elif url == "/api/v2/search":
            return mock_search_response
        raise ValueError(f"Unexpected URL: {url}")

    mock_client.post = AsyncMock(side_effect=mock_post)
    service._client = mock_client

    # Create a search request with distance=5
    request = SearchRequest(
        keywords="test",
        latitude=39.9366619061509,
        longitude=32.5859851407316,
        pages=0,
        size=24,
        distance=5,
    )

    await service.search(request)

    # Verify both API calls were made
    assert mock_client.post.call_count == 2

    # Verify the nearest API was called with distance=5
    first_call = mock_client.post.call_args_list[0]
    assert first_call[0][0] == "/api/v2/nearest"
    assert first_call[1]["json"]["distance"] == 5

    # Verify the search API was called with distance=5
    second_call = mock_client.post.call_args_list[1]
    assert second_call[0][0] == "/api/v2/search"
    assert second_call[1]["json"]["distance"] == 5
