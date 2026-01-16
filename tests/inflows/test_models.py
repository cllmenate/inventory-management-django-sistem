"""Tests for Inflows model."""

import pytest

from inflows.models import Inflows
from tests.factories import InflowFactory, ProductFactory, SupplierFactory


@pytest.mark.unit
@pytest.mark.django_db
class TestInflowsModel:
    """Test suite for Inflows model."""

    def test_inflow_creation(self):
        """Test creating an inflow with valid data."""
        product = ProductFactory()
        supplier = SupplierFactory()

        inflow = InflowFactory(
            product=product, supplier=supplier, quantity=50, description="Initial stock"
        )

        assert inflow.id is not None
        assert inflow.product == product
        assert inflow.supplier == supplier
        assert inflow.quantity == 50
        assert inflow.description == "Initial stock"

    def test_inflow_str_representation(self):
        """Test inflow string representation."""
        product = ProductFactory(title="Test Product")
        inflow = InflowFactory(product=product)

        assert str(inflow) == "Test Product"

    def test_inflow_ordering(self):
        """Test inflows are ordered by created_at descending."""
        inflow1 = InflowFactory()
        inflow2 = InflowFactory()
        inflow3 = InflowFactory()

        inflows = Inflows.objects.all()

        # Should be in descending order (newest first)
        assert inflows[0].created_at >= inflows[1].created_at
        assert inflows[1].created_at >= inflows[2].created_at

    def test_inflow_relationships(self):
        """Test inflow relationships are properly set."""
        inflow = InflowFactory()

        assert inflow.product is not None
        assert inflow.supplier is not None
        assert hasattr(inflow.product, "title")
        assert hasattr(inflow.supplier, "name")

    def test_inflow_verbose_names(self):
        """Test model verbose names."""
        assert Inflows._meta.verbose_name == "Entrada"
        assert Inflows._meta.verbose_name_plural == "Entradas"
