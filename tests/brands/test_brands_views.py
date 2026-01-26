import pytest
from django.urls import reverse
from unittest.mock import patch
from brands.models import Brand


@pytest.mark.django_db
class TestBrandViews:
    def test_brand_list_view(self, client, authenticated_user, brand):
        client.force_login(authenticated_user)
        url = reverse("brand_list")
        response = client.get(url)
        assert response.status_code == 200
        assert brand in response.context["brands"]

    def test_brand_list_view_filter(self, client, authenticated_user, brand):
        client.force_login(authenticated_user)
        url = reverse("brand_list")
        response = client.get(url, {"name": brand.name})
        assert response.status_code == 200
        assert brand in response.context["brands"]

        response = client.get(url, {"name": "NonExistent"})
        assert response.status_code == 200
        assert len(response.context["brands"]) == 0

    def test_brand_create_view(self, client, authenticated_user):
        client.force_login(authenticated_user)
        url = reverse("brand_create")
        data = {"name": "New Brand", "description": "Description"}
        response = client.post(url, data)
        assert response.status_code == 302
        assert Brand.objects.filter(name="New Brand").exists()

    def test_brand_detail_view(self, client, authenticated_user, brand):
        client.force_login(authenticated_user)
        url = reverse("brand_detail", kwargs={"pk": brand.pk})
        response = client.get(url)
        assert response.status_code == 200
        assert response.context["object"] == brand

    def test_brand_update_view(self, client, authenticated_user, brand):
        client.force_login(authenticated_user)
        url = reverse("brand_update", kwargs={"pk": brand.pk})
        data = {"name": "Updated Brand", "description": "Updated Description"}
        response = client.post(url, data)
        assert response.status_code == 302
        brand.refresh_from_db()
        assert brand.name == "Updated Brand"

    def test_brand_delete_view(self, client, authenticated_user, brand):
        client.force_login(authenticated_user)
        url = reverse("brand_delete", kwargs={"pk": brand.pk})
        response = client.post(url)
        assert response.status_code == 302
        assert not Brand.objects.filter(pk=brand.pk).exists()

    @patch("app.tasks.export_data_async.apply_async")
    def test_brand_export_view(self, mock_task, client, authenticated_user):
        client.force_login(authenticated_user)
        url = reverse("brand_export")
        mock_task.return_value.id = "fake-task-id"
        response = client.get(url, HTTP_REFERER="/previous/")
        assert response.status_code == 302
        mock_task.assert_called_once()
        from notifications.models import TaskNotification

        assert TaskNotification.objects.filter(
            task_type="export", model_name="Brand"
        ).exists()

    @patch("app.tasks.import_data_async.apply_async")
    def test_brand_import_view(self, mock_task, client, authenticated_user, tmp_path):
        client.force_login(authenticated_user)
        url = reverse("brand_import")
        file_path = tmp_path / "test.csv"
        file_path.write_text("dummy content", encoding="utf-8")
        with open(file_path, "rb") as f:
            mock_task.return_value.id = "fake-task-id"
            response = client.post(url, {"file": f}, HTTP_REFERER="/previous/")
            assert response.status_code == 302
            mock_task.assert_called_once()
            from notifications.models import TaskNotification

            assert TaskNotification.objects.filter(
                task_type="import", model_name="Brand"
            ).exists()


@pytest.mark.django_db
class TestBrandAPI:
    def test_brand_list_create_api(self, api_client, authenticated_user):
        api_client.force_authenticate(user=authenticated_user)
        url = reverse("brand_list_create_api_view")

        # List
        response = api_client.get(url)
        assert response.status_code == 200

        # Create
        data = {"name": "API Brand", "description": "API Description"}
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert Brand.objects.filter(name="API Brand").exists()

    def test_brand_retrieve_update_destroy_api(
        self, api_client, authenticated_user, brand
    ):
        api_client.force_authenticate(user=authenticated_user)
        url = reverse("brand_detail_api_view", kwargs={"pk": brand.pk})

        # Retrieve
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data["id"] == brand.id

        # Update
        data = {"name": "API Updated Brand", "description": "Updated"}
        response = api_client.put(url, data)
        assert response.status_code == 200
        brand.refresh_from_db()
        assert brand.name == "API Updated Brand"

        # Delete
        response = api_client.delete(url)
        assert response.status_code == 204
        assert not Brand.objects.filter(pk=brand.pk).exists()
