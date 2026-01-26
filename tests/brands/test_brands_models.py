"""Tests for Brand model."""

import pytest

from brands.models import Brand
from tests.factories import BrandFactory


@pytest.mark.unit
@pytest.mark.django_db
class TestBrandModel:
    """Test suite for Brand model."""

    def test_brand_creation_with_valid_data(self):
        """Test creating a brand with valid data."""
        brand = BrandFactory(name="Test Brand", description="Test Description")

        assert brand.id is not None
        assert brand.name == "Test Brand"
        assert brand.description == "Test Description"
        assert brand.created_at is not None
        assert brand.updated_at is not None

    def test_brand_str_representation(self):
        """Test brand string representation."""
        brand = BrandFactory(name="Nike")
        assert str(brand) == "Nike"

    def test_brand_creation_without_description(self):
        """Test creating a brand without description (nullable field)."""
        brand = BrandFactory(description=None)

        assert brand.id is not None
        assert brand.description is None

    def test_brand_ordering(self):
        """Test brands are ordered by name."""
        BrandFactory(name="Zebra")
        BrandFactory(name="Apple")
        BrandFactory(name="Microsoft")

        brands = Brand.objects.all()
        names = [brand.name for brand in brands]

        assert names == sorted(names)

    def test_brand_verbose_names(self):
        """Test model verbose names."""
        assert Brand._meta.verbose_name == "Marca"
        assert Brand._meta.verbose_name_plural == "Marcas"

    def test_brand_name_max_length(self):
        """Test brand name max length constraint."""
        long_name = "A" * 100  # Max is 100
        brand = BrandFactory(name=long_name)
        assert len(brand.name) == 100

    def test_brand_update_timestamp(self, brand):
        """Test that updated_at changes on save."""
        original_updated_at = brand.updated_at
        brand.name = "Updated Name"
        brand.save()
        brand.refresh_from_db()

        assert brand.updated_at > original_updated_at
