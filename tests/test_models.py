"""Tests for data models"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.models import (
    CategoriesResponse,
    Category,
    DepotLocation,
    FacetItem,
    FacetMap,
    NearestDepot,
    NearestDepotRequest,
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

    # Test distance validation
    with pytest.raises(ValidationError):
        SearchRequest(
            keywords="test",
            latitude=39.9366,
            longitude=32.5859,
            distance=0,  # Invalid: must be >= 1
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


def test_depot_location_model():
    """Test DepotLocation model"""
    location = DepotLocation(lon=32.588585, lat=39.941654)

    assert location.lon == 32.588585
    assert location.lat == 39.941654


def test_nearest_depot_model():
    """Test NearestDepot model"""
    depot = NearestDepot(
        id="bim-U751",
        sellerName="Saraycık Camisincan",
        location=DepotLocation(lon=32.588585, lat=39.941654),
        marketName="bim",
        distance=597.5797281730618,
    )

    assert depot.id == "bim-U751"
    assert depot.sellerName == "Saraycık Camisincan"
    assert depot.marketName == "bim"
    assert depot.distance == 597.5797281730618
    assert depot.location.lon == 32.588585
    assert depot.location.lat == 39.941654


def test_nearest_depot_request_validation():
    """Test NearestDepotRequest validation"""
    # Valid request
    request = NearestDepotRequest(
        latitude=39.9366619061509, longitude=32.5859851407316, distance=1
    )
    assert request.latitude == 39.9366619061509
    assert request.longitude == 32.5859851407316
    assert request.distance == 1

    # Test default distance
    request = NearestDepotRequest(latitude=39.9366, longitude=32.5859)
    assert request.distance == 1  # Default value

    # Test distance validation
    with pytest.raises(ValidationError):
        NearestDepotRequest(
            latitude=39.9366,
            longitude=32.5859,
            distance=0,  # Invalid: must be >= 1
        )


def test_category_model():
    """Test Category model"""
    category = Category(
        name="Meyve ve Sebze",
        subcategories=["Meyve", "Sebze"],
    )

    assert category.name == "Meyve ve Sebze"
    assert len(category.subcategories) == 2
    assert category.subcategories[0] == "Meyve"
    assert category.subcategories[1] == "Sebze"


def test_categories_response_model():
    """Test CategoriesResponse model"""
    response = CategoriesResponse(
        content=[
            Category(
                name="Meyve ve Sebze",
                subcategories=["Meyve", "Sebze"],
            ),
            Category(
                name="Süt Ürünleri ve Kahvaltılık",
                subcategories=["Süt", "Yumurta", "Peynir"],
            ),
        ]
    )

    assert len(response.content) == 2
    assert response.content[0].name == "Meyve ve Sebze"
    assert response.content[1].name == "Süt Ürünleri ve Kahvaltılık"
    assert len(response.content[1].subcategories) == 3
