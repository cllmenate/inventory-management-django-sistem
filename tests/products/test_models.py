"""Tests for Product model."""

from decimal import Decimal

import pytest

from products.models import Product
from tests.factories import CategoryFactory, ProductFactory, ProductModelFactory


@pytest.mark.unit
@pytest.mark.django_db
class TestProductModel:
    """Test suite for Product model."""

    def test_product_creation_with_all_fields(self):
        """Test creating a product with all fields."""
        product_model = ProductModelFactory()
        category = CategoryFactory()

        product = ProductFactory(
            title="Gaming Laptop",
            product_model=product_model,
            category=category,
            description="High-end gaming laptop",
            serial_number="SN123456",
            cost_price=Decimal("2000.00"),
            sell_price=Decimal("2500.00"),
            quantity=10,
        )

        assert product.id is not None
        assert product.title == "Gaming Laptop"
        assert product.product_model == product_model
        assert product.category == category
        assert product.cost_price == Decimal("2000.00")
        assert product.sell_price == Decimal("2500.00")
        assert product.quantity == 10

    def test_product_str_representation(self):
        """Test product string representation."""
        product = ProductFactory(title="Test Product")
        assert str(product) == "Test Product"

    def test_product_default_quantity_is_zero(self):
        """Test default quantity is 0."""
        product = ProductFactory()
        # Quantity is 0 by default in factory
        assert product.quantity == 0

    def test_product_relationships(self):
        """Test product has proper relationships."""
        product = ProductFactory()

        assert product.product_model is not None
        assert product.category is not None
        assert hasattr(product.product_model, "brand")

    def test_product_ordering(self):
        """Test products are ordered by title."""
        ProductFactory(title="Zebra Product")
        ProductFactory(title="Alpha Product")

        products = Product.objects.all()
        titles = [p.title for p in products]
        assert titles == sorted(titles)

    def test_product_verbose_names(self):
        """Test model verbose names."""
        assert Product._meta.verbose_name == "Produto"
        assert Product._meta.verbose_name_plural == "Produtos"

    def test_product_price_validation(self):
        """Test product prices are decimal fields."""
        product = ProductFactory(
            cost_price=Decimal("100.50"), sell_price=Decimal("150.75")
        )

        assert isinstance(product.cost_price, Decimal)
        assert isinstance(product.sell_price, Decimal)
        assert product.sell_price > product.cost_price
