import pytest

from product_models.serializers import ProductModelSerializer


@pytest.mark.django_db
class TestProductModelSerializers:
    def test_product_model_serializer_valid(self, brand):
        data = {
            "name": "Valid Model",
            "brand": brand.id,
            "description": "Description",
        }
        serializer = ProductModelSerializer(data=data)
        assert serializer.is_valid()
        instance = serializer.save()
        assert instance.name == "Valid Model"

    def test_product_model_serializer_invalid(self):
        data = {
            "name": "",
            "description": "Description",
        }
        serializer = ProductModelSerializer(data=data)
        assert not serializer.is_valid()
        assert "name" in serializer.errors
