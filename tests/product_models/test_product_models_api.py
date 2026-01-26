import pytest
from django.urls import reverse

from product_models.models import ProductModel


@pytest.mark.django_db
class TestProductModelAPI:
    def test_product_model_list_create_api(
        self, api_client, authenticated_user, brand
    ):
        api_client.force_authenticate(user=authenticated_user)
        url = reverse("product_model_list_create_api_view")

        # List
        response = api_client.get(url)
        assert response.status_code == 200

        # Create
        data = {
            "name": "API Model",
            "brand": brand.id,
            "description": "API",
        }
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert ProductModel.objects.filter(name="API Model").exists()

    def test_product_model_retrieve_update_destroy_api(
        self, api_client, authenticated_user, product_model
    ):
        api_client.force_authenticate(user=authenticated_user)
        url = reverse(
            "product_model_detail_api_view",
            kwargs={"pk": product_model.pk},
        )

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
