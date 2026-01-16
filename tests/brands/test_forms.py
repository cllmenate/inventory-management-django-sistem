"""Tests for Brand form."""

import pytest

from brands.forms import BrandForm


@pytest.mark.unit
class TestBrandForm:
    """Test suite for BrandForm."""

    def test_form_with_valid_data(self):
        """Test form with valid data."""
        data = {"name": "Form Brand", "description": "Form description"}
        form = BrandForm(data=data)

        assert form.is_valid()

    def test_form_without_name(self):
        """Test form without required name field."""
        data = {"description": "Only description"}
        form = BrandForm(data=data)

        assert not form.is_valid()
        assert "name" in form.errors

    def test_form_without_description(self):
        """Test form without optional description field."""
        data = {"name": "Name Only"}
        form = BrandForm(data=data)

        assert form.is_valid()

    def test_form_saves_brand(self):
        """Test form saves brand correctly."""
        data = {"name": "Saved Brand", "description": "Saved description"}
        form = BrandForm(data=data)

        assert form.is_valid()

    def test_form_field_labels(self):
        """Test form field labels are in Portuguese."""
        form = BrandForm()

        assert form.fields["name"].label == "Nome"
        assert form.fields["description"].label == "Descrição"

    def test_form_error_messages(self):
        """Test form error messages are in Portuguese."""
        data = {}
        form = BrandForm(data=data)

        assert not form.is_valid()
        assert "O nome é obrigatório" in str(form.errors["name"])

    def test_form_widget_classes(self):
        """Test form widgets have Bootstrap classes."""
        form = BrandForm()

        assert "form-control" in form.fields["name"].widget.attrs["class"]
        assert "form-control" in form.fields["description"].widget.attrs["class"]

    @pytest.mark.django_db
    def test_form_update_existing_brand(self, brand):
        """Test form can update existing brand."""
        data = {"name": "Updated via Form", "description": "Updated description"}
        form = BrandForm(data=data, instance=brand)

        assert form.is_valid()
        updated_brand = form.save()
        assert updated_brand.id == brand.id
        assert updated_brand.name == "Updated via Form"
