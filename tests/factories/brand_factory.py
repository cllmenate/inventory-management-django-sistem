"""Brand factory for testing."""

import factory

from brands.models import Brand


class BrandFactory(factory.django.DjangoModelFactory):
    """Factory for creating Brand instances."""

    class Meta:
        model = Brand
        django_get_or_create = ("name",)

    name = factory.Sequence(lambda n: f"Brand {n}")
    description = factory.Faker("text", max_nb_chars=200)
