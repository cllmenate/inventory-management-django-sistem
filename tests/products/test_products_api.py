import pytest
from django.urls import reverse

from products.models import Product


@pytest.mark.django_db
class TestProductAPI:
    def test_product_list_create_api(
        self, api_client, authenticated_user, category, product_model
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
