"""Fixtures for supplier tests."""

import pytest

from tests.factories import SupplierFactory


@pytest.fixture
def supplier():
    """Create a supplier instance."""
    return SupplierFactory()
