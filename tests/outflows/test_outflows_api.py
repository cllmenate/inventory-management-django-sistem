import pytest
from django.urls import reverse

from outflows.models import Outflows


@pytest.mark.django_db
class TestOutflowAPI:
    def test_outflow_list_create_api(
        self,
        api_client,
        authenticated_user,
        product_with_stock,
    ):
        api_client.force_authenticate(user=authenticated_user)
        url = reverse("outflow_list_create_api_view")

        # List
        response = api_client.get(url)
        assert response.status_code == 200

        # Create
        data = {
            "product": product_with_stock.id,
            "quantity": 2,
            "description": "API Outflow",
        }
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert Outflows.objects.filter(description="API Outflow").exists()

    def test_outflow_retrieve_api(
        self,
        api_client,
        authenticated_user,
        outflow,
    ):
        api_client.force_authenticate(user=authenticated_user)
        url = reverse("outflow_detail_api_view", kwargs={"pk": outflow.pk})
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data["id"] == outflow.id
