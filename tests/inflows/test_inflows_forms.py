import pytest

from inflows.forms import InflowForm


@pytest.mark.django_db
class TestInflowForms:
    def test_inflow_form_valid(self, supplier, product):
        data = {
            "supplier": supplier.id,
            "product": product.id,
            "quantity": 10,
            "description": "Description",
        }
        form = InflowForm(data=data)
        assert form.is_valid()

    def test_inflow_form_invalid(self):
        data = {}
        form = InflowForm(data=data)
        assert not form.is_valid()
        assert "quantity" in form.errors
