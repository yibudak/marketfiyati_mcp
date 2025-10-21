"""Tests for data models"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.models import (
    FacetItem,
    FacetMap,
    Product,
    ProductDepotInfo,
    SearchRequest,
    SearchResponse,
)


def test_search_request_validation():
    """Test SearchRequest validation"""
    # Valid request
    request = SearchRequest(
        keywords="test",
        latitude=39.9366,
        longitude=32.5859,
    )
    assert request.keywords == "test"
    assert request.latitude == 39.9366
    assert request.longitude == 32.5859

    # Test size validation
    with pytest.raises(ValidationError):
        SearchRequest(
            keywords="test",
            latitude=39.9366,
            longitude=32.5859,
            size=0,  # Invalid: must be >= 1
        )

    with pytest.raises(ValidationError):
        SearchRequest(
            keywords="test",
            latitude=39.9366,
            longitude=32.5859,
            size=101,  # Invalid: must be <= 100
        )


def test_product_depot_info_model():
    """Test ProductDepotInfo model"""
    depot_info = ProductDepotInfo(
        depotId="bim-D216",
        depotName="Test Depot",
        price=59.0,
        unitPrice="59,00 ₺/kg",
        marketAdi="bim",
        percentage=0.0,
        longitude=32.58121,
        latitude=39.94765,
        indexTime="20.10.2025 11:11",
    )

    assert depot_info.depotId == "bim-D216"
    assert depot_info.price == 59.0
    assert depot_info.marketAdi == "bim"


def test_product_model():
    """Test Product model"""
    product = Product(
        id="test123",
        title="Test Product",
        brand="Test Brand",
        imageUrl="https://example.com/image.jpg",
        refinedQuantityUnit="1 Adet",
        refinedVolumeOrWeight="1 kg",
        categories=["Category 1", "Category 2"],
        productDepotInfoList=[],
    )

    assert product.id == "test123"
    assert product.title == "Test Product"
    assert len(product.categories) == 2


def test_facet_item_model():
    """Test FacetItem model"""
    facet = FacetItem(name="Test Facet", count=10)

    assert facet.name == "Test Facet"
    assert facet.count == 10


def test_facet_map_model():
    """Test FacetMap model with optional fields"""
    # Empty facet map
    facet_map = FacetMap()
    assert facet_map.sub_category is None
    assert facet_map.brand is None

    # Facet map with some fields
    facet_map = FacetMap(
        sub_category=[FacetItem(name="Category 1", count=5)],
        brand=[FacetItem(name="Brand 1", count=10)],
    )
    assert len(facet_map.sub_category) == 1
    assert len(facet_map.brand) == 1


def test_search_response_model():
    """Test SearchResponse model"""
    response = SearchResponse(
        numberOfFound=100,
        searchResultType=1,
        content=[],
        facetMap=FacetMap(),
    )

    assert response.numberOfFound == 100
    assert response.searchResultType == 1
    assert len(response.content) == 0
