from unittest.mock import patch

import pytest
from django.urls import reverse

from products.models import Product


@pytest.mark.django_db
class TestProductViews:
    def test_product_list_view(self, client, authenticated_user, product):
        client.force_login(authenticated_user)
        url = reverse("product_list")
        response = client.get(url)
        assert response.status_code == 200
        assert product in response.context["products"]

    def test_product_list_view_filter(
        self, client, authenticated_user, product
    ):
        client.force_login(authenticated_user)
        url = reverse("product_list")
        response = client.get(url, {"title": product.title})
        assert response.status_code == 200
        assert product in response.context["products"]

        response = client.get(url, {"title": "NonExistent"})
        assert response.status_code == 200
        assert len(response.context["products"]) == 0

    def test_product_create_view(
        self, client, authenticated_user, category, product_model
    ):
        client.force_login(authenticated_user)
        url = reverse("product_create")
        data = {
            "title": "New Product",
            "category": category.id,
            "product_model": product_model.id,
            "description": "New Product Description",
            "serial_number": "SN123",
            "cost_price": 100,
            "sell_price": 200,
            "quantity": 10,
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert Product.objects.filter(title="New Product").exists()

    def test_product_detail_view(self, client, authenticated_user, product):
        client.force_login(authenticated_user)
        url = reverse("product_detail", kwargs={"pk": product.pk})
        response = client.get(url)
        assert response.status_code == 200
        assert response.context["object"] == product

    def test_product_update_view(self, client, authenticated_user, product):
        client.force_login(authenticated_user)
        url = reverse("product_update", kwargs={"pk": product.pk})
        data = {
            "title": "Updated Product",
            "category": product.category.id,
            "product_model": product.product_model.id,
            "description": "Updated Product Description",
            "serial_number": product.serial_number,
            "cost_price": 100,
            "sell_price": 200,
            "quantity": 10,
        }
        response = client.post(url, data)
        assert response.status_code == 302
        product.refresh_from_db()
        assert product.title == "Updated Product"

    def test_product_delete_view(self, client, authenticated_user, product):
        client.force_login(authenticated_user)
        url = reverse("product_delete", kwargs={"pk": product.pk})
        response = client.post(url)
        assert response.status_code == 302
        assert not Product.objects.filter(pk=product.pk).exists()

    @patch("app.tasks.export_data_async.apply_async")
    def test_product_export_view(self, mock_task, client, authenticated_user):
        client.force_login(authenticated_user)
        url = reverse("product_export")
        mock_task.return_value.id = "fake-task-id"
        response = client.get(url, HTTP_REFERER="/previous/")
        assert response.status_code == 302
        mock_task.assert_called_once()
        from notifications.models import TaskNotification

        assert TaskNotification.objects.filter(
            task_type="export", model_name="Product"
        ).exists()

    @patch("app.tasks.import_data_async.apply_async")
    def test_product_import_view(
        self, mock_task, client, authenticated_user, tmp_path
    ):
        client.force_login(authenticated_user)
        url = reverse("product_import")
        file_path = tmp_path / "test.csv"
        file_path.write_text("dummy content", encoding="utf-8")
        with open(file_path, "rb") as f:
            mock_task.return_value.id = "fake-task-id"
            response = client.post(url, {"file": f}, HTTP_REFERER="/previous/")
            assert response.status_code == 302
            mock_task.assert_called_once()
            from notifications.models import TaskNotification

            assert TaskNotification.objects.filter(
                task_type="import", model_name="Product"
            ).exists()


@pytest.mark.django_db
class TestProductAPI:
    def test_product_list_create_api(
        self, api_client, authenticated_user, brand, category, product_model
    ):
        api_client.force_authenticate(user=authenticated_user)
        url = reverse("product_list_create_api_view")

        # List
        response = api_client.get(url)
        assert response.status_code == 200

        # Create
        data = {
            "title": "API Product",
            "category": category.id,
            "product_model": product_model.id,
            "description": "API Product Description",
            "serial_number": "SNAPI123",
            "cost_price": 100,
            "sell_price": 200,
            "quantity": 10,
        }
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert Product.objects.filter(title="API Product").exists()

    def test_product_retrieve_update_destroy_api(
        self, api_client, authenticated_user, product
    ):
        api_client.force_authenticate(user=authenticated_user)
        url = reverse("product_detail_api_view", kwargs={"pk": product.pk})

        # Retrieve
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data["id"] == product.id

        # Update
        data = {
            "title": "API Updated Product",
            "category": product.category.id,
            "product_model": product.product_model.id,
            "description": "API Updated Product Description",
            "serial_number": product.serial_number,
            "cost_price": 100,
            "sell_price": 200,
            "quantity": 10,
        }
        response = api_client.put(url, data)
        assert response.status_code == 200
        product.refresh_from_db()
        assert product.title == "API Updated Product"

        # Delete
        response = api_client.delete(url)
        assert response.status_code == 204
        assert not Product.objects.filter(pk=product.pk).exists()
