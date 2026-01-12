"""Tests for Outflows signals - CRITICAL for inventory management."""

import pytest
from outflows.models import Outflows
from tests.factories import OutflowFactory, ProductFactory


@pytest.mark.signals
@pytest.mark.django_db
class TestOutflowSignals:
    """Test suite for Outflow signal handlers - critical for inventory."""

    def test_outflow_creation_decrements_product_quantity(self):
        """Test that creating an outflow decreases product quantity."""
        # Arrange: Create a product with initial quantity
        product = ProductFactory(quantity=100)
        initial_quantity = product.quantity

        # Act: Create an outflow
        outflow = OutflowFactory(product=product, quantity=25)

        # Assert: Product quantity should be decremented
        product.refresh_from_db()
        assert product.quantity == initial_quantity - 25
        assert product.quantity == 75

    def test_outflow_reduces_to_zero(self):
        """Test outflow can reduce product quantity to zero."""
        # Arrange
        product = ProductFactory(quantity=50)

        # Act
        outflow = OutflowFactory(product=product, quantity=50)

        # Assert
        product.refresh_from_db()
        assert product.quantity == 0

    def test_multiple_outflows_accumulate_decrements(self):
        """Test multiple outflows properly decrement quantity."""
        # Arrange
        product = ProductFactory(quantity=100)

        # Act: Create multiple outflows
        OutflowFactory(product=product, quantity=10)
        product.refresh_from_db()
        assert product.quantity == 90

        OutflowFactory(product=product, quantity=20)
        product.refresh_from_db()
        assert product.quantity == 70

        OutflowFactory(product=product, quantity=15)
        product.refresh_from_db()
        assert product.quantity == 55

    def test_outflow_signal_only_triggers_on_creation(self):
        """Test signal only triggers on creation, not on update."""
        # Arrange
        product = ProductFactory(quantity=100)

        # Act: Create outflow
        outflow = OutflowFactory(product=product, quantity=10)
        product.refresh_from_db()
        assert product.quantity == 90

        # Update the outflow (should not change product quantity)
        outflow.quantity = 50
        outflow.save()
        product.refresh_from_db()

        # Assert: Quantity should remain the same
        assert product.quantity == 90

    def test_outflow_can_create_negative_stock(self):
        """Test outflow allows negative stock (business logic may need validation)."""
        # Arrange: This tests current behavior - may need business logic to prevent
        product = ProductFactory(quantity=10)

        # Act: Create outflow larger than stock
        outflow = OutflowFactory(product=product, quantity=30)

        # Assert: Currently allows negative (might want to add validation)
        product.refresh_from_db()
        assert product.quantity == -20

    def test_outflow_different_products_independent(self):
        """Test outflows for different products are independent."""
        # Arrange
        product1 = ProductFactory(quantity=50)
        product2 = ProductFactory(quantity=80)

        # Act
        OutflowFactory(product=product1, quantity=10)
        OutflowFactory(product=product2, quantity=20)

        # Assert
        product1.refresh_from_db()
        product2.refresh_from_db()
        assert product1.quantity == 40
        assert product2.quantity == 60

    def test_outflow_with_large_quantity(self):
        """Test outflow handles large quantities correctly."""
        # Arrange
        product = ProductFactory(quantity=10000)

        # Act
        OutflowFactory(product=product, quantity=5000)

        # Assert
        product.refresh_from_db()
        assert product.quantity == 5000
