"""ProductModel factory for testing."""

import factory
from product_models.models import ProductModel
from tests.factories.brand_factory import BrandFactory


class ProductModelFactory(factory.django.DjangoModelFactory):
    """Factory for creating ProductModel instances."""

    class Meta:
        model = ProductModel

    name = factory.Sequence(lambda n: f"Model {n}")
    brand = factory.SubFactory(BrandFactory)
    description = factory.Faker("text", max_nb_chars=500)
