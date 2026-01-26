import pytest

from products.forms import ProductForm


@pytest.mark.django_db
class TestProductForms:
    def test_product_form_valid(self, category, product_model):
        data = {
            "title": "Valid Product",
            "category": category.id,
            "product_model": product_model.id,
            "serial_number": "SN123",
            "cost_price": 100,
            "sell_price": 200,
            "quantity": 10,
            "description": "Description",
        }
        form = ProductForm(data=data)
        assert form.is_valid()

    def test_product_form_invalid(self):
        data = {}
        form = ProductForm(data=data)
        assert not form.is_valid()
        assert "title" in form.errors
