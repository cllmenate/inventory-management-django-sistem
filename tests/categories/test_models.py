"""Tests for Category model."""

import pytest
from categories.models import Category
from tests.factories import CategoryFactory


@pytest.mark.unit
@pytest.mark.django_db
class TestCategoryModel:
    """Test suite for Category model."""

    def test_category_creation_with_valid_data(self):
        """Test creating a category with valid data."""
        category = CategoryFactory(
            name="Electronics", description="Electronic products"
        )

        assert category.id is not None
        assert category.name == "Electronics"
        assert category.description == "Electronic products"
        assert category.created_at is not None
        assert category.updated_at is not None

    def test_category_str_representation(self):
        """Test category string representation."""
        category = CategoryFactory(name="Sports")
        assert str(category) == "Sports"

    def test_category_creation_without_description(self):
        """Test creating a category without description."""
        category = CategoryFactory(description=None)

        assert category.id is not None
        assert category.description is None

    def test_category_ordering(self):
        """Test categories are ordered by name."""
        CategoryFactory(name="Zebra")
        CategoryFactory(name="Apple")
        CategoryFactory(name="Microsoft")

        categories = Category.objects.all()
        names = [cat.name for cat in categories]

        assert names == sorted(names)

    def test_category_verbose_names(self):
        """Test model verbose names."""
        assert Category._meta.verbose_name == "Categoria"
        assert Category._meta.verbose_name_plural == "Categorias"

    def test_category_update_timestamp(self, category):
        """Test that updated_at changes on save."""
        original_updated_at = category.updated_at
        category.name = "Updated Category"
        category.save()
        category.refresh_from_db()

        assert category.updated_at > original_updated_at
