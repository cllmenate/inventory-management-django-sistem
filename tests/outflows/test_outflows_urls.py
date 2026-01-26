import pytest  # noqa: F401
from django.urls import resolve, reverse

from outflows import views


class TestOutflowURLs:
    def test_list_url(self):
        url = reverse("outflow_list")
        assert resolve(url).func.view_class == views.OutflowListView

    def test_create_url(self):
        url = reverse("outflow_create")
        assert resolve(url).func.view_class == views.OutflowCreateView

    def test_detail_url(self):
        url = reverse("outflow_detail", kwargs={"pk": 1})
        assert resolve(url).func.view_class == views.OutflowDetailView

    def test_export_url(self):
        url = reverse("outflow_export")
        assert resolve(url).func.view_class == views.OutflowExportView

    def test_import_url(self):
        url = reverse("outflow_import")
        assert resolve(url).func.view_class == views.OutflowImportView
