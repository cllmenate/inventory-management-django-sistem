import pytest

from product_models.forms import ProductModelForm


@pytest.mark.django_db
class TestProductModelForms:
    def test_product_model_form_valid(self, brand):
        data = {
            "name": "Valid Model",
            "brand": brand.id,
            "description": "Description",
        }
        form = ProductModelForm(data=data)
        assert form.is_valid()

    def test_product_model_form_invalid(self):
        data = {
            "name": "",
            "description": "Description",
        }
        form = ProductModelForm(data=data)
        assert not form.is_valid()
        assert "name" in form.errors
