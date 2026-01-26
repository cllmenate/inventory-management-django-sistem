import pytest  # noqa: F401
from django.urls import resolve, reverse

from suppliers import views


class TestSupplierURLs:
    def test_list_url(self):
        url = reverse("supplier_list")
        assert resolve(url).func.view_class == views.SupplierListView

    def test_create_url(self):
        url = reverse("supplier_create")
        assert resolve(url).func.view_class == views.SupplierCreateView

    def test_detail_url(self):
        url = reverse("supplier_detail", kwargs={"pk": 1})
        assert resolve(url).func.view_class == views.SupplierDetailView

    def test_update_url(self):
        url = reverse("supplier_update", kwargs={"pk": 1})
        assert resolve(url).func.view_class == views.SupplierUpdateView

    def test_delete_url(self):
        url = reverse("supplier_delete", kwargs={"pk": 1})
        assert resolve(url).func.view_class == views.SupplierDeleteView

    def test_export_url(self):
        url = reverse("supplier_export")
        assert resolve(url).func.view_class == views.SupplierExportView

    def test_import_url(self):
        url = reverse("supplier_import")
        assert resolve(url).func.view_class == views.SupplierImportView
