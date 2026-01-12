"""Factory exports for easy imports."""

from tests.factories.user_factory import UserFactory
from tests.factories.brand_factory import BrandFactory
from tests.factories.category_factory import CategoryFactory
from tests.factories.supplier_factory import SupplierFactory
from tests.factories.product_model_factory import ProductModelFactory
from tests.factories.product_factory import ProductFactory
from tests.factories.inflow_factory import InflowFactory
from tests.factories.outflow_factory import OutflowFactory

__all__ = [
    "UserFactory",
    "BrandFactory",
    "CategoryFactory",
    "SupplierFactory",
    "ProductModelFactory",
    "ProductFactory",
    "InflowFactory",
    "OutflowFactory",
]
