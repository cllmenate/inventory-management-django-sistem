"""Tests for Supplier model."""

import pytest
from suppliers.models import Supplier
from tests.factories import SupplierFactory


@pytest.mark.unit
@pytest.mark.django_db
class TestSupplierModel:
    """Test suite for Supplier model."""

    def test_supplier_creation(self):
        """Test creating a supplier with valid data."""
        supplier = SupplierFactory(name="ABC Supplies")

        assert supplier.id is not None
        assert supplier.name == "ABC Supplies"

    def test_supplier_str_representation(self):
        """Test supplier string representation."""
        supplier = SupplierFactory(name="XYZ Corp")
        assert str(supplier) == "XYZ Corp"

    def test_supplier_ordering(self):
        """Test suppliers are ordered by name."""
        SupplierFactory(name="Zebra Corp")
        SupplierFactory(name="Alpha Inc")

        suppliers = Supplier.objects.all()
        names = [s.name for s in suppliers]
        assert names == sorted(names)
