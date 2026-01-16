"""Fixtures for category tests."""

import pytest

from tests.factories import CategoryFactory


@pytest.fixture
def category():
    """Create a category instance."""
    return CategoryFactory()


@pytest.fixture
def category_list():
    """Create a list of categories."""
    return CategoryFactory.create_batch(5)
