"""Supplier factory for testing."""

import factory

from suppliers.models import Supplier


class SupplierFactory(factory.django.DjangoModelFactory):
    """Factory for creating Supplier instances."""

    class Meta:
        model = Supplier
        django_get_or_create = ("name",)

    name = factory.Sequence(lambda n: f"Supplier {n}")
    description = factory.Faker("text", max_nb_chars=200)
