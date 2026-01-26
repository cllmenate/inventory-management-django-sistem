import pytest

from outflows.serializers import OutflowSerializer


@pytest.mark.django_db
class TestOutflowSerializers:
    def test_outflow_serializer_valid(self, product_with_stock):
        data = {
            "product": product_with_stock.id,
            "quantity": 5,
            "description": "Description",
        }
        serializer = OutflowSerializer(data=data)
        assert serializer.is_valid()
        outflow = serializer.save()
        assert outflow.quantity == 5

    def test_outflow_serializer_invalid(self):
        data = {}
        serializer = OutflowSerializer(data=data)
        assert not serializer.is_valid()
        assert "quantity" in serializer.errors
