from __future__ import annotations

from pydantic import BaseModel, Field


class NearestDepotRequest(BaseModel):
    """Request model for finding nearest depots"""

    latitude: float = Field(..., description="User latitude coordinate")
    longitude: float = Field(..., description="User longitude coordinate")
    distance: int = Field(default=1, ge=1, description="Search radius in kilometers")


class DepotLocation(BaseModel):
    """Depot location coordinates"""

    lon: float = Field(..., description="Longitude coordinate")
    lat: float = Field(..., description="Latitude coordinate")


class NearestDepot(BaseModel):
    """Information about a nearby depot"""

    id: str = Field(..., description="Unique depot identifier (e.g., 'bim-U751')")
    sellerName: str = Field(..., description="Depot/seller name")
    location: DepotLocation = Field(..., description="Depot location coordinates")
    marketName: str = Field(..., description="Market name (e.g., 'bim', 'a101')")
    distance: float = Field(..., description="Distance from user location in meters")


class SearchRequest(BaseModel):
    """Base request model for searching products"""

    keywords: str = Field(..., description="Search keywords or category name")
    latitude: float = Field(..., description="User latitude coordinate")
    longitude: float = Field(..., description="User longitude coordinate")
    pages: int = Field(default=0, ge=0, description="Page number for pagination")
    size: int = Field(
        default=24, ge=1, le=100, description="Number of results per page"
    )
    distance: int = Field(default=1, ge=1, description="Search radius in kilometers")


class SearchByCategoryRequest(SearchRequest):
    """Request model for searching products by categories (includes menuCategory)"""

    menuCategory: bool = Field(default=True, description="Search in menu categories")


class ProductDepotInfo(BaseModel):
    """Information about product availability in a specific depot"""

    depotId: str = Field(..., description="Unique depot identifier")
    depotName: str = Field(..., description="Human-readable depot name")
    price: float = Field(..., description="Product price")
    unitPrice: str = Field(..., description="Formatted unit price with currency")
    marketAdi: str = Field(..., description="Market name (e.g., bim, a101, migros)")
    percentage: float = Field(..., description="Discount percentage if any")
    longitude: float = Field(..., description="Depot longitude coordinate")
    latitude: float = Field(..., description="Depot latitude coordinate")
    indexTime: str = Field(..., description="Last index update time")


class Product(BaseModel):
    """Product information model"""

    id: str = Field(..., description="Unique product identifier")
    title: str = Field(..., description="Product title")
    brand: str = Field(..., description="Product brand")
    imageUrl: str = Field(..., description="Product image URL")
    refinedQuantityUnit: str | None = Field(
        default=None, description="Quantity unit (e.g., '1 Adet')"
    )
    refinedVolumeOrWeight: str | None = Field(
        default=None, description="Volume or weight (e.g., '1 kg')"
    )
    categories: list[str] = Field(..., description="Product categories")
    productDepotInfoList: list[ProductDepotInfo] = Field(
        ..., description="List of depot availability info"
    )


class FacetItem(BaseModel):
    """Facet item for filtering"""

    name: str = Field(..., description="Facet name")
    count: int = Field(..., description="Number of products matching this facet")


class FacetMap(BaseModel):
    """Facet map containing all available filters"""

    sub_category: list[FacetItem] | None = Field(
        default=None, description="Sub-category filters"
    )
    refined_quantity_unit: list[FacetItem] | None = Field(
        default=None, description="Quantity unit filters"
    )
    main_category: list[FacetItem] | None = Field(
        default=None, description="Main category filters"
    )
    refined_volume_weight: list[FacetItem] | None = Field(
        default=None, description="Volume/weight filters"
    )
    brand: list[FacetItem] | None = Field(default=None, description="Brand filters")
    market_names: list[FacetItem] | None = Field(
        default=None, description="Market name filters"
    )


class SearchResponse(BaseModel):
    """Response model for product search"""

    numberOfFound: int = Field(..., description="Total number of products found")
    searchResultType: int = Field(..., description="Type of search result")
    content: list[Product] = Field(..., description="List of products")
    facetMap: FacetMap = Field(..., description="Available filters and facets")


class Category(BaseModel):
    """Category information model"""

    name: str = Field(..., description="Main category name")
    subcategories: list[str] = Field(..., description="List of subcategory names")


class CategoriesResponse(BaseModel):
    """Response model for categories endpoint"""

    content: list[Category] = Field(..., description="List of categories")
