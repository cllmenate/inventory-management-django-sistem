import pytest
from django.urls import reverse

from categories.models import Category


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
