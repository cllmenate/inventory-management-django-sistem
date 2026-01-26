import pytest  # noqa: F401
from django.urls import resolve, reverse

from products import views


class TestProductURLs:
    def test_list_url(self):
        url = reverse("product_list")
        assert resolve(url).func.view_class == views.ProductListView

    def test_create_url(self):
        url = reverse("product_create")
        assert resolve(url).func.view_class == views.ProductCreateView

    def test_detail_url(self):
        url = reverse("product_detail", kwargs={"pk": 1})
        assert resolve(url).func.view_class == views.ProductDetailView

    def test_update_url(self):
        url = reverse("product_update", kwargs={"pk": 1})
        assert resolve(url).func.view_class == views.ProductUpdateView

    def test_delete_url(self):
        url = reverse("product_delete", kwargs={"pk": 1})
        assert resolve(url).func.view_class == views.ProductDeleteView

    def test_export_url(self):
        url = reverse("product_export")
        assert resolve(url).func.view_class == views.ProductExportView

    def test_import_url(self):
        url = reverse("product_import")
        assert resolve(url).func.view_class == views.ProductImportView
