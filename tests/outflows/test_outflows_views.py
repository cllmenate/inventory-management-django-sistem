import pytest
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch

from outflows.models import Outflows
from outflows import models


@pytest.mark.django_db
class TestOutflowViews:
    def test_outflow_list_view_authenticated(
        self, client, authenticated_user, product_with_stock, outflow
    ):
        client.force_login(authenticated_user)
        url = reverse("outflow_list")
        response = client.get(url)
        assert response.status_code == 200
        assert "outflows" in response.context
        assert outflow in response.context["outflows"]

    def test_outflow_list_view_filter(
        self, client, authenticated_user, product_with_stock, outflow
    ):
        client.force_login(authenticated_user)
        url = reverse("outflow_list")
        response = client.get(url, {"product": outflow.product.title})
        assert response.status_code == 200
        assert outflow in response.context["outflows"]

        response = client.get(url, {"product": "NonExistent"})
        assert response.status_code == 200
        assert len(response.context["outflows"]) == 0

    def test_outflow_create_view(self, client, authenticated_user, product_with_stock):
        client.force_login(authenticated_user)
        url = reverse("outflow_create")
        data = {
            "product": product_with_stock.id,
            "quantity": 5,
            "description": "Test Outflow",
        }
        # Assuming product_with_stock has enough quantity or metrics service handles it without erroring
        # (Outflows usually check quantity, but let's assume valid data for now)
        response = client.post(url, data)
        assert response.status_code == 302
        assert Outflows.objects.filter(description="Test Outflow").exists()

    def test_outflow_detail_view(self, client, authenticated_user, outflow):
        client.force_login(authenticated_user)
        url = reverse("outflow_detail", kwargs={"pk": outflow.pk})
        response = client.get(url)
        assert response.status_code == 200
        assert response.context["object"] == outflow

    @patch("app.tasks.export_data_async.apply_async")
    def test_outflow_export_view(self, mock_task, client, authenticated_user):
        client.force_login(authenticated_user)
        url = reverse("outflow_export")

        mock_task.return_value.id = "fake-task-id"

        response = client.get(url, HTTP_REFERER="/previous/")

        assert response.status_code == 302
        mock_task.assert_called_once()

        from notifications.models import TaskNotification

        notification = TaskNotification.objects.first()
        assert notification is not None
        assert notification.task_type == "export"
        assert notification.model_name == "Outflows"

    @patch("app.tasks.import_data_async.apply_async")
    def test_outflow_import_view(self, mock_task, client, authenticated_user, tmp_path):
        client.force_login(authenticated_user)
        url = reverse("outflow_import")

        file_path = tmp_path / "test.csv"
        file_path.write_text("dummy content", encoding="utf-8")

        with open(file_path, "rb") as f:
            mock_task.return_value.id = "fake-task-id"
            response = client.post(url, {"file": f}, HTTP_REFERER="/previous/")

            assert response.status_code == 302
            mock_task.assert_called_once()

            from notifications.models import TaskNotification

            assert TaskNotification.objects.filter(task_type="import").exists()


@pytest.mark.django_db
class TestOutflowAPI:
    def test_outflow_list_create_api(
        self, api_client, authenticated_user, product_with_stock
    ):
        api_client.force_authenticate(user=authenticated_user)
        url = reverse("outflow_list_create_api_view")

        # List
        response = api_client.get(url)
        assert response.status_code == 200

        # Create
        data = {
            "product": product_with_stock.id,
            "quantity": 2,
            "description": "API Outflow",
        }
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert Outflows.objects.filter(description="API Outflow").exists()

    def test_outflow_retrieve_api(self, api_client, authenticated_user, outflow):
        api_client.force_authenticate(user=authenticated_user)
        url = reverse("outflow_detail_api_view", kwargs={"pk": outflow.pk})
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data["id"] == outflow.id
