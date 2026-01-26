"""Fixtures for product tests."""

import pytest

from tests.factories import (
    BrandFactory,
    CategoryFactory,
    ProductFactory,
    ProductModelFactory,
)


@pytest.fixture
def product():
    """Create a product instance."""
    return ProductFactory()


@pytest.fixture
def product_with_stock():
    """Create a product with initial stock."""
    return ProductFactory(quantity=100)


@pytest.fixture
def product_model():
    """Create a product model for product tests."""
    return ProductModelFactory()


@pytest.fixture
def category():
    """Create a category for product tests."""
    return CategoryFactory()


@pytest.fixture
def brand():
    """Create a brand for product tests."""
    return BrandFactory()
