"""Product factory for testing."""

import factory
from decimal import Decimal
from products.models import Product
from tests.factories.product_model_factory import ProductModelFactory
from tests.factories.category_factory import CategoryFactory


class ProductFactory(factory.django.DjangoModelFactory):
    """Factory for creating Product instances."""

    class Meta:
        model = Product

    title = factory.Sequence(lambda n: f"Product {n}")
    product_model = factory.SubFactory(ProductModelFactory)
    category = factory.SubFactory(CategoryFactory)
    description = factory.Faker("text", max_nb_chars=500)
    serial_number = factory.Sequence(lambda n: f"SN{n:06d}")
    cost_price = factory.LazyFunction(lambda: Decimal("100.00"))
    sell_price = factory.LazyFunction(lambda: Decimal("150.00"))
    quantity = 0
