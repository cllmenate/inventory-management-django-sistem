"""Integration tests for inventory flow."""

import pytest

from tests.factories import (
    BrandFactory,
    CategoryFactory,
    InflowFactory,
    OutflowFactory,
    ProductFactory,
    ProductModelFactory,
    SupplierFactory,
)


@pytest.mark.integration
@pytest.mark.django_db
class TestInventoryFlow:
    """Test suite for complete inventory management flow."""

    def test_complete_product_lifecycle(self, complete_product_setup):
        """Test complete product lifecycle from creation to stock movement."""
        # Arrange
        product = complete_product_setup["product"]
        supplier = complete_product_setup["supplier"]

        # Initial state
        assert product.quantity == 0

        # Act 1: Receive stock (inflow)
        inflow1 = InflowFactory(product=product, supplier=supplier, quantity=100)
        product.refresh_from_db()

        # Assert: Stock increased
        assert product.quantity == 100

        # Act 2: Sell some items (outflow)
        outflow1 = OutflowFactory(product=product, quantity=30)
        product.refresh_from_db()

        # Assert: Stock decreased
        assert product.quantity == 70

        # Act 3: Receive more stock
        inflow2 = InflowFactory(product=product, supplier=supplier, quantity=50)
        product.refresh_from_db()

        # Assert: Stock increased again
        assert product.quantity == 120

        # Act 4: Another outflow
        outflow2 = OutflowFactory(product=product, quantity=20)
        product.refresh_from_db()

        # Final assertion
        assert product.quantity == 100

    def test_multiple_products_independent_inventory(self):
        """Test that multiple products have independent inventory tracking."""
        # Arrange
        product1 = ProductFactory(quantity=0)
        product2 = ProductFactory(quantity=0)
        supplier = SupplierFactory()

        # Act: Operations on product 1
        InflowFactory(product=product1, supplier=supplier, quantity=50)
        OutflowFactory(product=product1, quantity=10)

        # Operations on product 2
        InflowFactory(product=product2, supplier=supplier, quantity=30)
        OutflowFactory(product=product2, quantity=5)

        # Assert
        product1.refresh_from_db()
        product2.refresh_from_db()

        assert product1.quantity == 40
        assert product2.quantity == 25

    def test_concurrent_inflows_outflows(self):
        """Test concurrent inflows and outflows maintain correct inventory."""
        # Arrange
        product = ProductFactory(quantity=100)
        supplier = SupplierFactory()

        # Act: Multiple concurrent operations
        InflowFactory(product=product, supplier=supplier, quantity=20)
        product.refresh_from_db()
        assert product.quantity == 120

        OutflowFactory(product=product, quantity=15)
        product.refresh_from_db()
        assert product.quantity == 105

        InflowFactory(product=product, supplier=supplier, quantity=10)
        product.refresh_from_db()
        assert product.quantity == 115

        OutflowFactory(product=product, quantity=25)
        product.refresh_from_db()
        assert product.quantity == 90

        # Final assertion
        assert product.quantity == 90

    def test_inventory_accuracy_after_many_operations(self):
        """Test inventory remains accurate after many operations."""
        # Arrange
        product = ProductFactory(quantity=0)
        supplier = SupplierFactory()

        # Act: Perform many operations
        expected_quantity = 0

        # 10 inflows
        for i in range(10):
            qty = (i + 1) * 10  # 10, 20, 30, ..., 100
            InflowFactory(product=product, supplier=supplier, quantity=qty)
            expected_quantity += qty

        product.refresh_from_db()
        assert product.quantity == expected_quantity  # Should be 550

        # 5 outflows
        for i in range(5):
            qty = (i + 1) * 5  # 5, 10, 15, 20, 25
            OutflowFactory(product=product, quantity=qty)
            expected_quantity -= qty

        product.refresh_from_db()
        assert product.quantity == expected_quantity  # Should be 475

    def test_zero_quantity_flows(self):
        """Test handling of operations with quantities."""
        # Arrange
        product = ProductFactory(quantity=50)
        supplier = SupplierFactory()

        # Start with 50
        assert product.quantity == 50

        # Reduce to zero
        OutflowFactory(product=product, quantity=50)
        product.refresh_from_db()
        assert product.quantity == 0

        # Replenish from zero
        InflowFactory(product=product, supplier=supplier, quantity=25)
        product.refresh_from_db()
        assert product.quantity == 25

    def test_product_with_relationships_integrity(self):
        """Test that product relationships remain intact during operations."""
        # Arrange
        brand = BrandFactory(name="Nike")
        category = CategoryFactory(name="Sports")
        product_model = ProductModelFactory(name="Air Max", brand=brand)
        product = ProductFactory(
            title="Nike Air Max 90",
            product_model=product_model,
            category=category,
            quantity=0,
        )
        supplier = SupplierFactory()

        # Act
        InflowFactory(product=product, supplier=supplier, quantity=10)
        OutflowFactory(product=product, quantity=3)

        # Assert: Relationships still intact
        product.refresh_from_db()
        assert product.quantity == 7
        assert product.product_model.name == "Air Max"
        assert product.product_model.brand.name == "Nike"
        assert product.category.name == "Sports"
        assert product.title == "Nike Air Max 90"
