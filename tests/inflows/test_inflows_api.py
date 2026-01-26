import pytest
from django.urls import reverse

from inflows.models import Inflows


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
