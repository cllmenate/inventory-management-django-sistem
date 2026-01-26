import pytest
from django.urls import reverse

from suppliers.models import Supplier


@pytest.mark.django_db
class TestSupplierAPI:
    def test_supplier_list_create_api(self, api_client, authenticated_user):
        api_client.force_authenticate(user=authenticated_user)
        url = reverse("supplier_list_create_api_view")

        # List
        response = api_client.get(url)
        assert response.status_code == 200

        # Create
        data = {
            "name": "API Supplier",
            "email": "api@test.com",
            "description": "API",
        }
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
