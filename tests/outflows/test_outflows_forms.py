import pytest

from outflows.forms import OutflowForm


@pytest.mark.django_db
class TestOutflowForms:
    def test_outflow_form_valid(self, product_with_stock):
        data = {
            "product": product_with_stock.id,
            "quantity": 5,
            "description": "Description",
        }
        form = OutflowForm(data=data)
        assert form.is_valid()

    def test_outflow_form_invalid(self):
        data = {}
        form = OutflowForm(data=data)
        assert not form.is_valid()
        assert "quantity" in form.errors
