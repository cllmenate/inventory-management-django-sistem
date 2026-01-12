"""Fixtures for product model tests."""

import pytest
from tests.factories import ProductModelFactory, BrandFactory


@pytest.fixture
def product_model():
    """Create a product model instance."""
    return ProductModelFactory()


@pytest.fixture
def brand():
    """Create a brand for product model tests."""
    return BrandFactory()
