import pytest
from django.urls import reverse
from unittest.mock import patch
from suppliers.models import Supplier


@pytest.mark.django_db
class TestSupplierViews:
    def test_supplier_list_view(self, client, authenticated_user, supplier):
        client.force_login(authenticated_user)
        url = reverse("supplier_list")
        response = client.get(url)
        assert response.status_code == 200
        assert supplier in response.context["suppliers"]

    def test_supplier_list_view_filter(self, client, authenticated_user, supplier):
        client.force_login(authenticated_user)
        url = reverse("supplier_list")
        response = client.get(url, {"name": supplier.name})
        assert response.status_code == 200
        assert supplier in response.context["suppliers"]

        response = client.get(url, {"name": "NonExistent"})
        assert response.status_code == 200
        assert len(response.context["suppliers"]) == 0

    def test_supplier_create_view(self, client, authenticated_user):
        client.force_login(authenticated_user)
        url = reverse("supplier_create")
        data = {"name": "New Supplier", "email": "sup@test.com", "description": "Desc"}
        response = client.post(url, data)
        assert response.status_code == 302
        assert Supplier.objects.filter(name="New Supplier").exists()

    def test_supplier_detail_view(self, client, authenticated_user, supplier):
        client.force_login(authenticated_user)
        url = reverse("supplier_detail", kwargs={"pk": supplier.pk})
        response = client.get(url)
        assert response.status_code == 200
        assert response.context["object"] == supplier

    def test_supplier_update_view(self, client, authenticated_user, supplier):
        client.force_login(authenticated_user)
        url = reverse("supplier_update", kwargs={"pk": supplier.pk})
        data = {
            "name": "Updated Supplier",
            "email": "updated@test.com",
            "description": "Updated",
        }
        response = client.post(url, data)
        assert response.status_code == 302
        supplier.refresh_from_db()
        assert supplier.name == "Updated Supplier"

    def test_supplier_delete_view(self, client, authenticated_user, supplier):
        client.force_login(authenticated_user)
        url = reverse("supplier_delete", kwargs={"pk": supplier.pk})
        response = client.post(url)
        assert response.status_code == 302
        assert not Supplier.objects.filter(pk=supplier.pk).exists()

    @patch("app.tasks.export_data_async.apply_async")
    def test_supplier_export_view(self, mock_task, client, authenticated_user):
        client.force_login(authenticated_user)
        url = reverse("supplier_export")
        mock_task.return_value.id = "fake-task-id"
        response = client.get(url, HTTP_REFERER="/previous/")
        assert response.status_code == 302
        mock_task.assert_called_once()
        from notifications.models import TaskNotification

        assert TaskNotification.objects.filter(
            task_type="export", model_name="Supplier"
        ).exists()

    @patch("app.tasks.import_data_async.apply_async")
    def test_supplier_import_view(
        self, mock_task, client, authenticated_user, tmp_path
    ):
        client.force_login(authenticated_user)
        url = reverse("supplier_import")
        file_path = tmp_path / "test.csv"
        file_path.write_text("dummy content", encoding="utf-8")
        with open(file_path, "rb") as f:
            mock_task.return_value.id = "fake-task-id"
            response = client.post(url, {"file": f}, HTTP_REFERER="/previous/")
            assert response.status_code == 302
            mock_task.assert_called_once()
            from notifications.models import TaskNotification

            assert TaskNotification.objects.filter(
                task_type="import", model_name="Supplier"
            ).exists()


@pytest.mark.django_db
class TestSupplierAPI:
    def test_supplier_list_create_api(self, api_client, authenticated_user):
        api_client.force_authenticate(user=authenticated_user)
        url = reverse("supplier_list_create_api_view")

        # List
        response = api_client.get(url)
        assert response.status_code == 200

        # Create
        data = {"name": "API Supplier", "email": "api@test.com", "description": "API"}
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert Supplier.objects.filter(name="API Supplier").exists()

    def test_supplier_retrieve_update_destroy_api(
        self, api_client, authenticated_user, supplier
    ):
        api_client.force_authenticate(user=authenticated_user)
        url = reverse("supplier_detail_api_view", kwargs={"pk": supplier.pk})

        # Retrieve
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data["id"] == supplier.id

        # Update
        data = {
            "name": "API Updated Supplier",
            "email": "api@test.com",
            "description": "Updated",
        }
        response = api_client.put(url, data)
        assert response.status_code == 200
        supplier.refresh_from_db()
        assert supplier.name == "API Updated Supplier"

        # Delete
        response = api_client.delete(url)
        assert response.status_code == 204
        assert not Supplier.objects.filter(pk=supplier.pk).exists()
