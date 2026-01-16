"""Fixtures for integration tests."""

import pytest

from tests.factories import (
    BrandFactory,
    CategoryFactory,
    ProductFactory,
    ProductModelFactory,
    SupplierFactory,
)


@pytest.fixture
def complete_product_setup():
    """Create a complete product with all relationships."""
    brand = BrandFactory(name="Test Brand")
    category = CategoryFactory(name="Test Category")
    product_model = ProductModelFactory(name="Test Model", brand=brand)
    product = ProductFactory(
        title="Test Product", product_model=product_model, category=category, quantity=0
    )
    supplier = SupplierFactory(name="Test Supplier")

    return {
        "brand": brand,
        "category": category,
        "product_model": product_model,
        "product": product,
        "supplier": supplier,
    }
