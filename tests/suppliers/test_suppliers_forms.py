import pytest

from suppliers.forms import SupplierForm


@pytest.mark.django_db
class TestSupplierForms:
    def test_supplier_form_valid(self):
        data = {
            "name": "Valid Supplier",
            "email": "sup@test.com",
            "description": "Description",
        }
        form = SupplierForm(data=data)
        assert form.is_valid()

    def test_supplier_form_invalid(self):
        data = {
            "name": "",
            "email": "sup@test.com",
            "description": "Description",
        }
        form = SupplierForm(data=data)
        assert not form.is_valid()
        assert "name" in form.errors
