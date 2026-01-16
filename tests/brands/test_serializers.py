"""Tests for Brand serializer."""

import pytest

from brands.serializers import BrandSerializer


@pytest.mark.unit
@pytest.mark.django_db
class TestBrandSerializer:
    """Test suite for BrandSerializer."""

    def test_serialize_brand(self, brand):
        """Test serializing a brand instance."""
        serializer = BrandSerializer(brand)
        data = serializer.data

        assert data["id"] == brand.id
        assert data["name"] == brand.name
        assert data["description"] == brand.description
        assert "created_at" in data
        assert "updated_at" in data

    def test_deserialize_valid_data(self):
        """Test deserializing valid data."""
        data = {"name": "Serialized Brand", "description": "Test description"}
        serializer = BrandSerializer(data=data)

        assert serializer.is_valid()
        brand = serializer.save()
        assert brand.name == "Serialized Brand"
        assert brand.description == "Test description"

    def test_deserialize_without_description(self):
        """Test deserializing without optional description."""
        data = {"name": "Brand Without Description"}
        serializer = BrandSerializer(data=data)

        assert serializer.is_valid()
        brand = serializer.save()
        assert brand.name == "Brand Without Description"

    def test_serialize_multiple_brands(self, brand_list):
        """Test serializing multiple brands."""
        serializer = BrandSerializer(brand_list, many=True)
        data = serializer.data

        assert len(data) == 5
        assert all("id" in item for item in data)
        assert all("name" in item for item in data)
