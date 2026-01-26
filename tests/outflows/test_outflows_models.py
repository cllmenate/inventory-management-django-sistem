"""Tests for Outflows model."""

import pytest

from outflows.models import Outflows
from tests.factories import OutflowFactory, ProductFactory


@pytest.mark.unit
@pytest.mark.django_db
class TestOutflowsModel:
    """Test suite for Outflows model."""

    def test_outflow_creation(self):
        """Test creating an outflow with valid data."""
        product = ProductFactory(quantity=100)

        outflow = OutflowFactory(product=product, quantity=10, description="Sale")

        assert outflow.id is not None
        assert outflow.product == product
        assert outflow.quantity == 10
        assert outflow.description == "Sale"

    def test_outflow_str_representation(self):
        """Test outflow string representation."""
        product = ProductFactory(title="Test Product")
        outflow = OutflowFactory(product=product)

        assert str(outflow) == "Test Product"

    def test_outflow_ordering(self):
        """Test outflows are ordered by created_at descending."""
        outflow1 = OutflowFactory()
        outflow2 = OutflowFactory()
        outflow3 = OutflowFactory()

        outflows = Outflows.objects.all()

        # Should be in descending order (newest first)
        assert outflows[0].created_at >= outflows[1].created_at
        assert outflows[1].created_at >= outflows[2].created_at

    def test_outflow_verbose_names(self):
        """Test model verbose names."""
        assert Outflows._meta.verbose_name == "Saída"
        assert Outflows._meta.verbose_name_plural == "Saídas"
