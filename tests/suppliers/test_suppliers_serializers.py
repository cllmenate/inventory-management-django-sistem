import pytest

from suppliers.serializers import SupplierSerializer


@pytest.mark.django_db
class TestSupplierSerializers:
    def test_supplier_serializer_valid(self):
        data = {
            "name": "Valid Supplier",
            "email": "sup@test.com",
            "description": "Description",
        }
        serializer = SupplierSerializer(data=data)
        assert serializer.is_valid()
        supplier = serializer.save()
        assert supplier.name == "Valid Supplier"

    def test_supplier_serializer_invalid(self):
        data = {
            "name": "",
            "email": "sup@test.com",
            "description": "Description",
        }
        serializer = SupplierSerializer(data=data)
        assert not serializer.is_valid()
        assert "name" in serializer.errors
