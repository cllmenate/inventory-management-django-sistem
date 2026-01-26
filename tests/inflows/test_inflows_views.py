import pytest
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch

from inflows.models import Inflows
from inflows import models


@pytest.mark.django_db
class TestInflowViews:
    def test_inflow_list_view_authenticated(
        self, client, authenticated_user, product, inflow
    ):
        client.force_login(authenticated_user)
        url = reverse("inflow_list")
        response = client.get(url)
        assert response.status_code == 200
        assert "inflows" in response.context
        assert inflow in response.context["inflows"]

    def test_inflow_list_view_filter(self, client, authenticated_user, product, inflow):
        client.force_login(authenticated_user)
        url = reverse("inflow_list")
        response = client.get(url, {"product": inflow.product.title})
        assert response.status_code == 200
        assert inflow in response.context["inflows"]

        response = client.get(url, {"product": "NonExistent"})
        assert response.status_code == 200
        assert len(response.context["inflows"]) == 0

    def test_inflow_create_view(self, client, authenticated_user, product, supplier):
        client.force_login(authenticated_user)
        url = reverse("inflow_create")
        data = {
            "supplier": supplier.id,
            "product": product.id,
            "quantity": 10,
            "description": "Test Inflow",
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert Inflows.objects.filter(description="Test Inflow").exists()

    def test_inflow_detail_view(self, client, authenticated_user, inflow):
        client.force_login(authenticated_user)
        url = reverse("inflow_detail", kwargs={"pk": inflow.pk})
        response = client.get(url)
        assert response.status_code == 200
        assert response.context["object"] == inflow

    @patch("app.tasks.export_data_async.apply_async")
    def test_inflow_export_view(self, mock_task, client, authenticated_user):
        client.force_login(authenticated_user)
        url = reverse("inflow_export")

        # Configure the mock to return an object with an 'id' attribute
        mock_task.return_value.id = "fake-task-id"

        response = client.get(url, HTTP_REFERER="/previous/")

        # Verify redirect
        assert response.status_code == 302

        # Verify task passed to Celery
        mock_task.assert_called_once()

        # Verify notification created
        from notifications.models import TaskNotification

        notification = TaskNotification.objects.first()
        assert notification is not None
        assert notification.task_type == "export"
        assert notification.model_name == "Inflows"

    @patch("app.tasks.import_data_async.apply_async")
    def test_inflow_import_view(self, mock_task, client, authenticated_user, tmp_path):
        client.force_login(authenticated_user)
        url = reverse("inflow_import")

        # Create dummy file
        file_path = tmp_path / "test.csv"
        file_path.write_text("dummy content", encoding="utf-8")

        with open(file_path, "rb") as f:
            # Mock return value
            mock_task.return_value.id = "fake-task-id"

            response = client.post(url, {"file": f}, HTTP_REFERER="/previous/")

            assert response.status_code == 302
            mock_task.assert_called_once()

            from notifications.models import TaskNotification

            assert TaskNotification.objects.filter(task_type="import").exists()


@pytest.mark.django_db
class TestInflowAPI:
    def test_inflow_list_create_api(
        self, api_client, authenticated_user, supplier, product
    ):
        api_client.force_authenticate(user=authenticated_user)
        url = reverse("inflow_list_create_api_view")

        # List
        response = api_client.get(url)
        assert response.status_code == 200

        # Create
        data = {
            "supplier": supplier.id,
            "product": product.id,
            "quantity": 5,
            "description": "API Inflow",
        }
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert Inflows.objects.filter(description="API Inflow").exists()

    def test_inflow_retrieve_api(self, api_client, authenticated_user, inflow):
        api_client.force_authenticate(user=authenticated_user)
        url = reverse("inflow_detail_api_view", kwargs={"pk": inflow.pk})
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data["id"] == inflow.id
