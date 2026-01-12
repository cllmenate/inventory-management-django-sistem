"""Tests for Brand API endpoints."""

import pytest
from django.urls import reverse
from rest_framework import status
from brands.models import Brand
from tests.factories import BrandFactory


@pytest.mark.api
@pytest.mark.django_db
class TestBrandListCreateAPIView:
    """Test suite for Brand List/Create API."""

    def test_list_brands_requires_authentication(self, api_client):
        """Test listing brands requires authentication."""
        url = reverse("brand_list_create_api_view")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_brands_with_authentication(self, authenticated_client, brand_list):
        """Test listing brands with authentication."""
        url = reverse("brand_list_create_api_view")
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 5

    def test_create_brand_with_valid_data(self, authenticated_client):
        """Test creating brand via API with valid data."""
        url = reverse("brand_list_create_api_view")
        data = {"name": "API Brand", "description": "Created via API"}
        response = authenticated_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert Brand.objects.filter(name="API Brand").exists()
        assert response.data["name"] == "API Brand"

    def test_create_brand_without_authentication(self, api_client):
        """Test creating brand without authentication fails."""
        url = reverse("brand_list_create_api_view")
        data = {"name": "Unauthorized Brand", "description": "Should fail"}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_brand_without_permission(self, client_without_permissions):
        """Test creating brand without proper permissions."""
        url = reverse("brand_list_create_api_view")
        data = {"name": "No Permission Brand", "description": "Should fail"}
        response = client_without_permissions.post(url, data, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.api
@pytest.mark.django_db
class TestBrandRetrieveUpdateDestroyAPIView:
    """Test suite for Brand Retrieve/Update/Destroy API."""

    def test_retrieve_brand(self, authenticated_client, brand):
        """Test retrieving a specific brand."""
        url = reverse("brand_detail_api_view", kwargs={"pk": brand.pk})
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == brand.name
        assert response.data["id"] == brand.id

    def test_update_brand_with_valid_data(self, authenticated_client, brand):
        """Test updating brand via API."""
        url = reverse("brand_detail_api_view", kwargs={"pk": brand.pk})
        data = {"name": "Updated via API", "description": "Updated description"}
        response = authenticated_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        brand.refresh_from_db()
        assert brand.name == "Updated via API"

    def test_partial_update_brand(self, authenticated_client, brand):
        """Test partial update (PATCH) of brand."""
        url = reverse("brand_detail_api_view", kwargs={"pk": brand.pk})
        data = {"name": "Patched Name"}
        response = authenticated_client.patch(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        brand.refresh_from_db()
        assert brand.name == "Patched Name"

    def test_delete_brand(self, authenticated_client, brand):
        """Test deleting brand via API."""
        brand_id = brand.id
        url = reverse("brand_detail_api_view", kwargs={"pk": brand.pk})
        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Brand.objects.filter(id=brand_id).exists()

    def test_retrieve_nonexistent_brand(self, authenticated_client):
        """Test retrieving non-existent brand returns 404."""
        url = reverse("brand_detail_api_view", kwargs={"pk": 99999})
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
