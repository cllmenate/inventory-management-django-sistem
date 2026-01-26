import pytest

from categories.serializers import CategorySerializer


@pytest.mark.django_db
class TestCategorySerializers:
    def test_category_serializer_valid(self):
        data = {"name": "Valid Category", "description": "Description"}
        serializer = CategorySerializer(data=data)
        assert serializer.is_valid()
        category = serializer.save()
        assert category.name == "Valid Category"

    def test_category_serializer_invalid(self):
        data = {"name": "", "description": "Description"}
        serializer = CategorySerializer(data=data)
        assert not serializer.is_valid()
        assert "name" in serializer.errors
