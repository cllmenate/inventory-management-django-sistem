"""Fixtures for outflow tests."""

import pytest

from tests.factories import OutflowFactory, ProductFactory


@pytest.fixture
def outflow():
    """Create an outflow instance."""
    return OutflowFactory()


@pytest.fixture
def product_with_stock():
    """Create a product with stock for outflow tests."""
    return ProductFactory(quantity=100)
