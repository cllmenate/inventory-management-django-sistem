"""Tests for Inflows signals - CRITICAL for inventory management."""

import pytest

from tests.factories import InflowFactory, ProductFactory, SupplierFactory


@pytest.mark.signals
@pytest.mark.django_db
class TestInflowSignals:
    """Test suite for Inflow signal handlers - critical for inventory."""

    def test_inflow_creation_increments_product_quantity(self):
        """Test that creating an inflow increases product quantity."""
        # Arrange: Create a product with initial quantity
        product = ProductFactory(quantity=10)
        supplier = SupplierFactory()
        initial_quantity = product.quantity

        # Act: Create an inflow
        inflow = InflowFactory(product=product, supplier=supplier, quantity=25)

        # Assert: Product quantity should be incremented
        product.refresh_from_db()
        assert product.quantity == initial_quantity + 25
        assert product.quantity == 35

    def test_inflow_with_zero_quantity_product(self):
        """Test inflow on product with zero quantity."""
        # Arrange
        product = ProductFactory(quantity=0)
        supplier = SupplierFactory()

        # Act
        inflow = InflowFactory(product=product, supplier=supplier, quantity=100)

        # Assert
        product.refresh_from_db()
        assert product.quantity == 100

    def test_multiple_inflows_accumulate_quantity(self):
        """Test multiple inflows properly accumulate quantity."""
        # Arrange
        product = ProductFactory(quantity=0)
        supplier = SupplierFactory()

        # Act: Create multiple inflows
        InflowFactory(product=product, supplier=supplier, quantity=10)
        product.refresh_from_db()
        assert product.quantity == 10

        InflowFactory(product=product, supplier=supplier, quantity=20)
        product.refresh_from_db()
        assert product.quantity == 30

        InflowFactory(product=product, supplier=supplier, quantity=15)
        product.refresh_from_db()
        assert product.quantity == 45

    def test_inflow_signal_only_triggers_on_creation(self):
        """Test signal only triggers on creation, not on update."""
        # Arrange
        product = ProductFactory(quantity=10)
        supplier = SupplierFactory()

        # Act: Create inflow
        inflow = InflowFactory(product=product, supplier=supplier, quantity=5)
        product.refresh_from_db()
        assert product.quantity == 15

        # Update the inflow (should not change product quantity)
        inflow.quantity = 100
        inflow.save()
        product.refresh_from_db()

        # Assert: Quantity should remain the same
        assert product.quantity == 15

    def test_inflow_with_large_quantity(self):
        """Test inflow handles large quantities correctly."""
        # Arrange
        product = ProductFactory(quantity=1000)
        supplier = SupplierFactory()

        # Act
        InflowFactory(product=product, supplier=supplier, quantity=9999)

        # Assert
        product.refresh_from_db()
        assert product.quantity == 10999

    def test_inflow_different_products_independent(self):
        """Test inflows for different products are independent."""
        # Arrange
        product1 = ProductFactory(quantity=10)
        product2 = ProductFactory(quantity=20)
        supplier = SupplierFactory()

        # Act
        InflowFactory(product=product1, supplier=supplier, quantity=5)
        InflowFactory(product=product2, supplier=supplier, quantity=10)

        # Assert
        product1.refresh_from_db()
        product2.refresh_from_db()
        assert product1.quantity == 15
        assert product2.quantity == 30
