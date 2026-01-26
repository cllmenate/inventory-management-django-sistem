import pytest  # noqa: F401
from django.urls import resolve, reverse

from brands import views


class TestBrandURLs:
    def test_list_url(self):
        url = reverse("brand_list")
        assert resolve(url).func.view_class == views.BrandListView

    def test_create_url(self):
        url = reverse("brand_create")
        assert resolve(url).func.view_class == views.BrandCreateView

    def test_detail_url(self):
        url = reverse("brand_detail", kwargs={"pk": 1})
        assert resolve(url).func.view_class == views.BrandDetailView

    def test_update_url(self):
        url = reverse("brand_update", kwargs={"pk": 1})
        assert resolve(url).func.view_class == views.BrandUpdateView

    def test_delete_url(self):
        url = reverse("brand_delete", kwargs={"pk": 1})
        assert resolve(url).func.view_class == views.BrandDeleteView

    def test_export_url(self):
        url = reverse("brand_export")
        assert resolve(url).func.view_class == views.BrandExportView

    def test_import_url(self):
        url = reverse("brand_import")
        assert resolve(url).func.view_class == views.BrandImportView
