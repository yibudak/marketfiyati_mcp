"""Tests for health check endpoint"""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Test the health check endpoint returns healthy status"""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "marketfiyat-mcp"
    assert "version" in data


def test_health_check_response_structure(client: TestClient):
    """Test the health check response has the correct structure"""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "service" in data
    assert "version" in data
    assert isinstance(data["status"], str)
    assert isinstance(data["service"], str)
    assert isinstance(data["version"], str)


def test_version_endpoint(client: TestClient):
    """Test the version endpoint returns the API version"""
    response = client.get("/version")

    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert isinstance(data["version"], str)
    assert data["version"] == "1.0.0"
