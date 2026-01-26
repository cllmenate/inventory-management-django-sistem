import pytest

from categories.forms import CategoryForm


@pytest.mark.django_db
class TestCategoryForms:
    def test_category_form_valid(self):
        data = {"name": "Valid Category", "description": "Description"}
        form = CategoryForm(data=data)
        assert form.is_valid()

    def test_category_form_invalid(self):
        data = {"name": "", "description": "Description"}
        form = CategoryForm(data=data)
        assert not form.is_valid()
        assert "name" in form.errors
