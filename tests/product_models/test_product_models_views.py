import pytest
from django.urls import reverse
from unittest.mock import patch
from product_models.models import ProductModel


@pytest.mark.django_db
class TestProductModelViews:
    def test_product_model_list_view(self, client, authenticated_user, product_model):
        client.force_login(authenticated_user)
        url = reverse("product_model_list")
        response = client.get(url)
        assert response.status_code == 200
        assert product_model in response.context["product_models"]

    def test_product_model_list_view_filter(
        self, client, authenticated_user, product_model
    ):
        client.force_login(authenticated_user)
        url = reverse("product_model_list")
        response = client.get(url, {"name": product_model.name})
        assert response.status_code == 200
        assert product_model in response.context["product_models"]

        response = client.get(url, {"name": "NonExistent"})
        assert response.status_code == 200
        assert len(response.context["product_models"]) == 0

    def test_product_model_create_view(self, client, authenticated_user, brand):
        client.force_login(authenticated_user)
        url = reverse("product_model_create")
        data = {"name": "New Model", "brand": brand.id, "description": "Desc"}
        response = client.post(url, data)
        assert response.status_code == 302
        assert ProductModel.objects.filter(name="New Model").exists()

    def test_product_model_detail_view(self, client, authenticated_user, product_model):
        client.force_login(authenticated_user)
        url = reverse("product_model_detail", kwargs={"pk": product_model.pk})
        response = client.get(url)
        assert response.status_code == 200
        assert response.context["object"] == product_model

    def test_product_model_update_view(self, client, authenticated_user, product_model):
        client.force_login(authenticated_user)
        url = reverse("product_model_update", kwargs={"pk": product_model.pk})
        # Note: product_model fixture might include brand.
        data = {
            "name": "Updated Model",
            "brand": product_model.brand.id,
            "description": "Updated",
        }
        response = client.post(url, data)
        assert response.status_code == 302
        product_model.refresh_from_db()
        assert product_model.name == "Updated Model"

    def test_product_model_delete_view(self, client, authenticated_user, product_model):
        client.force_login(authenticated_user)
        url = reverse("product_model_delete", kwargs={"pk": product_model.pk})
        response = client.post(url)
        assert response.status_code == 302
        assert not ProductModel.objects.filter(pk=product_model.pk).exists()

    @patch("app.tasks.export_data_async.apply_async")
    def test_product_model_export_view(self, mock_task, client, authenticated_user):
        client.force_login(authenticated_user)
        url = reverse("product_model_export")
        mock_task.return_value.id = "fake-task-id"
        response = client.get(url, HTTP_REFERER="/previous/")
        assert response.status_code == 302
        mock_task.assert_called_once()
        from notifications.models import TaskNotification

        assert TaskNotification.objects.filter(
            task_type="export", model_name="ProductModel"
        ).exists()

    @patch("app.tasks.import_data_async.apply_async")
    def test_product_model_import_view(
        self, mock_task, client, authenticated_user, tmp_path
    ):
        client.force_login(authenticated_user)
        url = reverse("product_model_import")
        file_path = tmp_path / "test.csv"
        file_path.write_text("dummy content", encoding="utf-8")
        with open(file_path, "rb") as f:
            mock_task.return_value.id = "fake-task-id"
            response = client.post(url, {"file": f}, HTTP_REFERER="/previous/")
            assert response.status_code == 302
            mock_task.assert_called_once()
            from notifications.models import TaskNotification

            assert TaskNotification.objects.filter(
                task_type="import", model_name="ProductModel"
            ).exists()


@pytest.mark.django_db
class TestProductModelAPI:
    def test_product_model_list_create_api(self, api_client, authenticated_user, brand):
        api_client.force_authenticate(user=authenticated_user)
        url = reverse("product_model_list_create_api_view")

        # List
        response = api_client.get(url)
        assert response.status_code == 200

        # Create
        data = {"name": "API Model", "brand": brand.id, "description": "API"}
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert ProductModel.objects.filter(name="API Model").exists()

    def test_product_model_retrieve_update_destroy_api(
        self, api_client, authenticated_user, product_model
    ):
        api_client.force_authenticate(user=authenticated_user)
        url = reverse("product_model_detail_api_view", kwargs={"pk": product_model.pk})

        # Retrieve
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data["id"] == product_model.id

        # Update
        data = {
            "name": "API Updated Model",
            "brand": product_model.brand.id,
            "description": "Updated",
        }
        response = api_client.put(url, data)
        assert response.status_code == 200
        product_model.refresh_from_db()
        assert product_model.name == "API Updated Model"

        # Delete
        response = api_client.delete(url)
        assert response.status_code == 204
        assert not ProductModel.objects.filter(pk=product_model.pk).exists()
