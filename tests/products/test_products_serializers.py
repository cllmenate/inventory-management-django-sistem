import pytest

from products.serializers import ProductSerializer


@pytest.mark.django_db
class TestProductSerializers:
    def test_product_serializer_valid(self, category, product_model):
        data = {
            "title": "Valid Product",
            "category": category.id,
            "product_model": product_model.id,
            "serial_number": "SN123",
            "cost_price": 100,
            "sell_price": 200,
            "quantity": 10,
            "description": "Description",
        }
        serializer = ProductSerializer(data=data)
        assert serializer.is_valid()
        product = serializer.save()
        assert product.title == "Valid Product"

    def test_product_serializer_invalid(self):
        data = {}
        serializer = ProductSerializer(data=data)
        assert not serializer.is_valid()
        assert "title" in serializer.errors
