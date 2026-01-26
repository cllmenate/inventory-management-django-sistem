import pytest  # noqa: F401
from django.urls import resolve, reverse

from categories import views


class TestCategoryURLs:
    def test_list_url(self):
        url = reverse("category_list")
        assert resolve(url).func.view_class == views.CategoryListView

    def test_create_url(self):
        url = reverse("category_create")
        assert resolve(url).func.view_class == views.CategoryCreateView

    def test_detail_url(self):
        url = reverse("category_detail", kwargs={"pk": 1})
        assert resolve(url).func.view_class == views.CategoryDetailView

    def test_update_url(self):
        url = reverse("category_update", kwargs={"pk": 1})
        assert resolve(url).func.view_class == views.CategoryUpdateView

    def test_delete_url(self):
        url = reverse("category_delete", kwargs={"pk": 1})
        assert resolve(url).func.view_class == views.CategoryDeleteView

    def test_export_url(self):
        url = reverse("category_export")
        assert resolve(url).func.view_class == views.CategoryExportView

    def test_import_url(self):
        url = reverse("category_import")
        assert resolve(url).func.view_class == views.CategoryImportView
