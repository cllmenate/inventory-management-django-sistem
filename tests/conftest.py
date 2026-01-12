"""Global test fixtures and configuration."""

import pytest
from django.contrib.auth.models import User, Permission
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def api_client():
    """Return an API client instance."""
    return APIClient()


@pytest.fixture
def authenticated_user(db):
    """Create a user with all permissions."""
    user = User.objects.create_user(
        username="testuser", email="testuser@test.com", password="testpass123"
    )
    # Add all permissions
    permissions = Permission.objects.all()
    user.user_permissions.set(permissions)
    user.is_staff = True
    user.save()
    return user


@pytest.fixture
def authenticated_client(api_client, authenticated_user):
    """Return an authenticated API client."""
    refresh = RefreshToken.for_user(authenticated_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return api_client


@pytest.fixture
def user_without_permissions(db):
    """Create a user without any permissions."""
    return User.objects.create_user(
        username="nopermuser", email="noperm@test.com", password="testpass123"
    )


@pytest.fixture
def client_without_permissions(api_client, user_without_permissions):
    """Return an authenticated API client without permissions."""
    refresh = RefreshToken.for_user(user_without_permissions)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return api_client
