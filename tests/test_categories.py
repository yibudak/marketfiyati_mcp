"""Tests for categories endpoint"""

from __future__ import annotations

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.models import CategoriesResponse, Category


@pytest.fixture
def mock_categories_response():
    """Create a mock categories response"""
    return CategoriesResponse(
        content=[
            Category(
                name="Meyve ve Sebze",
                subcategories=["Meyve", "Sebze"],
            ),
            Category(
                name="Süt Ürünleri ve Kahvaltılık",
                subcategories=["Süt", "Yumurta", "Peynir", "Yoğurt"],
            ),
        ]
    )


def test_get_categories(client: TestClient, mock_categories_response):
    """Test GET categories endpoint"""
    with patch(
        "app.services.marketfiyat_service.MarketfiyatService.get_categories"
    ) as mock_get_categories:
        mock_get_categories.return_value = mock_categories_response

        response = client.get("/categories")

        assert response.status_code == 200
        data = response.json()
        assert "content" in data
        assert len(data["content"]) == 2
        assert data["content"][0]["name"] == "Meyve ve Sebze"
        assert len(data["content"][0]["subcategories"]) == 2
        assert data["content"][1]["name"] == "Süt Ürünleri ve Kahvaltılık"
        assert len(data["content"][1]["subcategories"]) == 4
