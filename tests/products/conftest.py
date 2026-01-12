"""Fixtures for product tests."""

import pytest
from decimal import Decimal
from tests.factories import ProductFactory, ProductModelFactory, CategoryFactory


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
