"""Fixtures for inflow tests."""

import pytest

from tests.factories import InflowFactory, ProductFactory, SupplierFactory


@pytest.fixture
def inflow():
    """Create an inflow instance."""
    return InflowFactory()


@pytest.fixture
def product():
    """Create a product for inflow tests."""
    return ProductFactory(quantity=0)


@pytest.fixture
def supplier():
    """Create a supplier for inflow tests."""
    return SupplierFactory()
