"""Tests for ProductModel model."""

import pytest

from product_models.models import ProductModel
from tests.factories import BrandFactory, ProductModelFactory


@pytest.mark.unit
@pytest.mark.django_db
class TestProductModelModel:
    """Test suite for ProductModel model."""

    def test_product_model_creation_with_brand(self):
        """Test creating a product model with brand."""
        brand = BrandFactory(name="Sony")
        product_model = ProductModelFactory(name="PlayStation 5", brand=brand)

        assert product_model.id is not None
        assert product_model.name == "PlayStation 5"
        assert product_model.brand == brand

    def test_product_model_str_representation(self):
        """Test product model string representation."""
        brand = BrandFactory(name="Apple")
        product_model = ProductModelFactory(name="iPhone 15", brand=brand)

        assert str(product_model) == "iPhone 15 - Apple"

    def test_product_model_brand_relationship(self):
        """Test brand foreign key relationship."""
        product_model = ProductModelFactory()

        assert product_model.brand is not None
        assert hasattr(product_model.brand, "name")

    def test_product_model_ordering(self):
        """Test product models are ordered by name."""
        ProductModelFactory(name="Zebra Model")
        ProductModelFactory(name="Alpha Model")

        models = ProductModel.objects.all()
        names = [m.name for m in models]
        assert names == sorted(names)

    def test_product_model_verbose_names(self):
        """Test model verbose names."""
        assert ProductModel._meta.verbose_name == "Modelo de Produto"
        assert ProductModel._meta.verbose_name_plural == "Modelos de Produto"
