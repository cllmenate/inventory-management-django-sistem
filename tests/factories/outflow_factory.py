"""Outflow factory for testing."""

import factory

from outflows.models import Outflows
from tests.factories.product_factory import ProductFactory


class OutflowFactory(factory.django.DjangoModelFactory):
    """Factory for creating Outflows instances."""

    class Meta:
        model = Outflows

    product = factory.SubFactory(ProductFactory)
    quantity = 5
    description = factory.Faker("text", max_nb_chars=200)
