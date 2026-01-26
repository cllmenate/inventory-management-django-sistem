import pytest
from inflows.serializers import InflowSerializer
from inflows.models import Inflows


@pytest.mark.django_db
class TestInflowSerializers:
    def test_inflow_serializer_valid(self, supplier, product):
        data = {
            "supplier": supplier.id,
            "product": product.id,
            "quantity": 10,
            "description": "Description",
        }
        serializer = InflowSerializer(data=data)
        assert serializer.is_valid()
        inflow = serializer.save()
        assert inflow.quantity == 10

    def test_inflow_serializer_invalid(self):
        data = {}
        serializer = InflowSerializer(data=data)
        assert not serializer.is_valid()
        assert "quantity" in serializer.errors
