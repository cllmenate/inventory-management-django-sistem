"""Category factory for testing."""

import factory

from categories.models import Category


class CategoryFactory(factory.django.DjangoModelFactory):
    """Factory for creating Category instances."""

    class Meta:
        model = Category
        django_get_or_create = ("name",)

    name = factory.Sequence(lambda n: f"Category {n}")
    description = factory.Faker("text", max_nb_chars=200)
