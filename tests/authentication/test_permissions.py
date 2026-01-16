"""Tests for DRF permissions."""

import pytest
from django.contrib.auth.models import Permission, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
class TestDRFPermissions:
    """Test suite for Django REST Framework permissions."""

    def test_authenticated_user_required(self):
        """Test that authentication is required for protected endpoints."""
        client = APIClient()
        url = reverse("brand_list_create_api_view")
        response = client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_with_permissions_can_access(self):
        """Test user with proper permissions can access endpoints."""
        # Create user with permissions
        user = User.objects.create_user(username="testuser", password="testpass123")
        permissions = Permission.objects.all()
        user.user_permissions.set(permissions)

        # Authenticate
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        # Access endpoint
        url = reverse("brand_list_create_api_view")
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_user_without_permissions_denied(self):
        """Test user without permissions is denied access."""
        # Create user without permissions
        user = User.objects.create_user(username="noperm", password="testpass123")

        # Authenticate
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        # Try to create brand (requires add_brand permission)
        url = reverse("brand_list_create_api_view")
        data = {"name": "Test Brand"}
        response = client.post(url, data, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_model_permissions_enforced(self):
        """Test Django model permissions are enforced."""
        # Create user
        user = User.objects.create_user(username="limiteduser", password="testpass123")

        # Add only view permission
        view_permission = Permission.objects.get(codename="view_brand")
        user.user_permissions.add(view_permission)

        # Authenticate
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        # Can view (GET)
        url = reverse("brand_list_create_api_view")
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

        # Cannot create (POST)
        data = {"name": "Test Brand"}
        response = client.post(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
