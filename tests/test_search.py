"""Tests for search endpoints"""

from __future__ import annotations

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.models import (
    FacetMap,
    Product,
    ProductDepotInfo,
    SearchByCategoryRequest,
    SearchRequest,
    SearchResponse,
)


@pytest.fixture
def mock_search_response():
    """Create a mock search response"""
    return SearchResponse(
        numberOfFound=1,
        searchResultType=1,
        content=[
            Product(
                id="test123",
                title="Test Product",
                brand="Test Brand",
                imageUrl="https://example.com/image.jpg",
                refinedQuantityUnit="1 Adet",
                refinedVolumeOrWeight="1 kg",
                categories=["Test Category"],
                productDepotInfoList=[
                    ProductDepotInfo(
                        depotId="test-depot",
                        depotName="Test Depot",
                        price=10.0,
                        unitPrice="10,00 ₺",
                        marketAdi="test",
                        percentage=0.0,
                        longitude=32.5,
                        latitude=39.9,
                        indexTime="2025-01-01 00:00",
                    )
                ],
            )
        ],
        facetMap=FacetMap(),
    )


def test_search_post(client: TestClient, mock_search_response):
    """Test POST search endpoint (without menuCategory)"""
    with patch(
        "app.services.marketfiyat_service.MarketfiyatService.search"
    ) as mock_search:
        mock_search.return_value = mock_search_response

        response = client.post(
            "/search",
            json={
                "keywords": "test",
                "latitude": 39.9366,
                "longitude": 32.5859,
                "pages": 0,
                "size": 24,
                "distance": 1,
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["numberOfFound"] == 1
        assert len(data["content"]) == 1
        assert data["content"][0]["title"] == "Test Product"


def test_search_get(client: TestClient, mock_search_response):
    """Test GET search endpoint (without menuCategory)"""
    with patch(
        "app.services.marketfiyat_service.MarketfiyatService.search"
    ) as mock_search:
        mock_search.return_value = mock_search_response

        response = client.get(
            "/search",
            params={
                "keywords": "test",
                "latitude": 39.9366,
                "longitude": 32.5859,
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["numberOfFound"] == 1


def test_search_by_categories_post(client: TestClient, mock_search_response):
    """Test POST search by categories endpoint (with menuCategory)"""
    with patch(
        "app.services.marketfiyat_service.MarketfiyatService.search_by_categories"
    ) as mock_search:
        mock_search.return_value = mock_search_response

        response = client.post(
            "/search_by_categories",
            json={
                "keywords": "test",
                "latitude": 39.9366,
                "longitude": 32.5859,
                "pages": 0,
                "size": 24,
                "menuCategory": True,
                "distance": 1,
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["numberOfFound"] == 1
        assert len(data["content"]) == 1
        assert data["content"][0]["title"] == "Test Product"


def test_search_by_categories_get(client: TestClient, mock_search_response):
    """Test GET search by categories endpoint"""
    with patch(
        "app.services.marketfiyat_service.MarketfiyatService.search_by_categories"
    ) as mock_search:
        mock_search.return_value = mock_search_response

        response = client.get(
            "/search_by_categories",
            params={
                "keywords": "test",
                "latitude": 39.9366,
                "longitude": 32.5859,
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["numberOfFound"] == 1


def test_search_by_categories_validation_error(client: TestClient):
    """Test search endpoint with missing required parameters"""
    response = client.post(
        "/search_by_categories",
        json={
            "keywords": "test",
            # Missing latitude and longitude
        },
    )

    assert response.status_code == 422  # Validation error


def test_search_by_categories_get_validation_error(client: TestClient):
    """Test GET search endpoint with missing required parameters"""
    response = client.get(
        "/search_by_categories",
        params={
            "keywords": "test",
            # Missing latitude and longitude
        },
    )

    assert response.status_code == 422  # Validation error


def test_search_request_defaults():
    """Test SearchRequest model default values (without menuCategory)"""
    request = SearchRequest(
        keywords="test",
        latitude=39.9366,
        longitude=32.5859,
    )

    assert request.pages == 0
    assert request.size == 24
    assert request.distance == 1


def test_search_request_custom_values():
    """Test SearchRequest model with custom values (without menuCategory)"""
    request = SearchRequest(
        keywords="test",
        latitude=39.9366,
        longitude=32.5859,
        pages=2,
        size=50,
        distance=10,
    )

    assert request.pages == 2
    assert request.size == 50
    assert request.distance == 10


def test_search_by_category_request_defaults():
    """Test SearchByCategoryRequest model default values (with menuCategory)"""
    request = SearchByCategoryRequest(
        keywords="test",
        latitude=39.9366,
        longitude=32.5859,
    )

    assert request.pages == 0
    assert request.size == 24
    assert request.menuCategory is True
    assert request.distance == 1


def test_search_by_category_request_custom_values():
    """Test SearchByCategoryRequest model with custom values (with menuCategory)"""
    request = SearchByCategoryRequest(
        keywords="test",
        latitude=39.9366,
        longitude=32.5859,
        pages=2,
        size=50,
        menuCategory=False,
        distance=10,
    )

    assert request.pages == 2
    assert request.size == 50
    assert request.menuCategory is False
    assert request.distance == 10
