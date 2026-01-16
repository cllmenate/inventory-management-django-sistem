"""Inflow factory for testing."""

import factory

from inflows.models import Inflows
from tests.factories.product_factory import ProductFactory
from tests.factories.supplier_factory import SupplierFactory


class InflowFactory(factory.django.DjangoModelFactory):
    """Factory for creating Inflows instances."""

    class Meta:
        model = Inflows

    supplier = factory.SubFactory(SupplierFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = 10
    description = factory.Faker("text", max_nb_chars=200)
