"""Fixtures for brand tests."""

import pytest

from tests.factories import BrandFactory


@pytest.fixture
def brand():
    """Create a brand instance."""
    return BrandFactory()


@pytest.fixture
def brand_list():
    """Create a list of brands."""
    return BrandFactory.create_batch(5)
