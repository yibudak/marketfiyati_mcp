"""Pytest configuration and fixtures"""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def app() -> FastAPI:
    """Create a test FastAPI application"""
    return create_app()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    """Create a test client"""
    return TestClient(app)
