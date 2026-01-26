import pytest  # noqa: F401
from django.urls import resolve, reverse

from inflows import views


class TestInflowURLs:
    def test_list_url(self):
        url = reverse("inflow_list")
        assert resolve(url).func.view_class == views.InflowListView

    def test_create_url(self):
        url = reverse("inflow_create")
        assert resolve(url).func.view_class == views.InflowCreateView

    def test_detail_url(self):
        url = reverse("inflow_detail", kwargs={"pk": 1})
        assert resolve(url).func.view_class == views.InflowDetailView

    def test_export_url(self):
        url = reverse("inflow_export")
        assert resolve(url).func.view_class == views.InflowExportView

    def test_import_url(self):
        url = reverse("inflow_import")
        assert resolve(url).func.view_class == views.InflowImportView
