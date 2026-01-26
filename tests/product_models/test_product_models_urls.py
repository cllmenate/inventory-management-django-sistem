import pytest  # noqa: F401
from django.urls import resolve, reverse

from product_models import views


class TestProductModelURLs:
    def test_list_url(self):
        url = reverse("product_model_list")
        assert resolve(url).func.view_class == views.ProductModelListView

    def test_create_url(self):
        url = reverse("product_model_create")
        assert resolve(url).func.view_class == views.ProductModelCreateView

    def test_detail_url(self):
        url = reverse("product_model_detail", kwargs={"pk": 1})
        assert resolve(url).func.view_class == views.ProductModelDetailView

    def test_update_url(self):
        url = reverse("product_model_update", kwargs={"pk": 1})
        assert resolve(url).func.view_class == views.ProductModelUpdateView

    def test_delete_url(self):
        url = reverse("product_model_delete", kwargs={"pk": 1})
        assert resolve(url).func.view_class == views.ProductModelDeleteView

    def test_export_url(self):
        url = reverse("product_model_export")
        assert resolve(url).func.view_class == views.ProductModelExportView

    def test_import_url(self):
        url = reverse("product_model_import")
        assert resolve(url).func.view_class == views.ProductModelImportView
