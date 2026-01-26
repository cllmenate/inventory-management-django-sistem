import pytest
from django.urls import reverse
from unittest.mock import patch
from categories.models import Category


@pytest.mark.django_db
class TestCategoryViews:
    def test_category_list_view(self, client, authenticated_user, category):
        client.force_login(authenticated_user)
        url = reverse("category_list")
        response = client.get(url)
        assert response.status_code == 200
        assert category in response.context["categories"]

    def test_category_list_view_filter(self, client, authenticated_user, category):
        client.force_login(authenticated_user)
        url = reverse("category_list")
        response = client.get(url, {"name": category.name})
        assert response.status_code == 200
        assert category in response.context["categories"]

        response = client.get(url, {"name": "NonExistent"})
        assert response.status_code == 200
        assert len(response.context["categories"]) == 0

    def test_category_create_view(self, client, authenticated_user):
        client.force_login(authenticated_user)
        url = reverse("category_create")
        data = {"name": "New Category", "description": "Description"}
        response = client.post(url, data)
        assert response.status_code == 302
        assert Category.objects.filter(name="New Category").exists()

    def test_category_detail_view(self, client, authenticated_user, category):
        client.force_login(authenticated_user)
        url = reverse("category_detail", kwargs={"pk": category.pk})
        response = client.get(url)
        assert response.status_code == 200
        assert response.context["object"] == category

    def test_category_update_view(self, client, authenticated_user, category):
        client.force_login(authenticated_user)
        url = reverse("category_update", kwargs={"pk": category.pk})
        data = {"name": "Updated Category", "description": "Updated Description"}
        response = client.post(url, data)
        assert response.status_code == 302
        category.refresh_from_db()
        assert category.name == "Updated Category"

    def test_category_delete_view(self, client, authenticated_user, category):
        client.force_login(authenticated_user)
        url = reverse("category_delete", kwargs={"pk": category.pk})
        response = client.post(url)
        assert response.status_code == 302
        assert not Category.objects.filter(pk=category.pk).exists()

    @patch("app.tasks.export_data_async.apply_async")
    def test_category_export_view(self, mock_task, client, authenticated_user):
        client.force_login(authenticated_user)
        url = reverse("category_export")
        mock_task.return_value.id = "fake-task-id"
        response = client.get(url, HTTP_REFERER="/previous/")
        assert response.status_code == 302
        mock_task.assert_called_once()
        from notifications.models import TaskNotification

        assert TaskNotification.objects.filter(
            task_type="export", model_name="Category"
        ).exists()

    @patch("app.tasks.import_data_async.apply_async")
    def test_category_import_view(
        self, mock_task, client, authenticated_user, tmp_path
    ):
        client.force_login(authenticated_user)
        url = reverse("category_import")
        file_path = tmp_path / "test.csv"
        file_path.write_text("dummy content", encoding="utf-8")
        with open(file_path, "rb") as f:
            mock_task.return_value.id = "fake-task-id"
            response = client.post(url, {"file": f}, HTTP_REFERER="/previous/")
            assert response.status_code == 302
            mock_task.assert_called_once()
            from notifications.models import TaskNotification

            assert TaskNotification.objects.filter(
                task_type="import", model_name="Category"
            ).exists()


@pytest.mark.django_db
class TestCategoryAPI:
    def test_category_list_create_api(self, api_client, authenticated_user):
        api_client.force_authenticate(user=authenticated_user)
        url = reverse("category_list_create_api_view")

        # List
        response = api_client.get(url)
        assert response.status_code == 200

        # Create
        data = {"name": "API Category", "description": "API Description"}
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert Category.objects.filter(name="API Category").exists()

    def test_category_retrieve_update_destroy_api(
        self, api_client, authenticated_user, category
    ):
        api_client.force_authenticate(user=authenticated_user)
        url = reverse("category_detail_api_view", kwargs={"pk": category.pk})

        # Retrieve
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data["id"] == category.id

        # Update
        data = {"name": "API Updated Category", "description": "Updated"}
        response = api_client.put(url, data)
        assert response.status_code == 200
        category.refresh_from_db()
        assert category.name == "API Updated Category"

        # Delete
        response = api_client.delete(url)
        assert response.status_code == 204
        assert not Category.objects.filter(pk=category.pk).exists()
