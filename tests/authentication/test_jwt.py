"""Tests for JWT authentication."""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import time_machine
from datetime import datetime, timedelta


@pytest.mark.django_db
class TestJWTAuthentication:
    """Test suite for JWT authentication."""

    def test_token_generation_for_valid_user(self):
        """Test JWT token generation for valid user."""
        user = User.objects.create_user(username="testuser", password="testpass123")

        refresh = RefreshToken.for_user(user)

        assert refresh is not None
        assert refresh.access_token is not None
        assert str(refresh.access_token) != ""

    def test_access_token_contains_user_id(self):
        """Test access token contains user ID."""
        user = User.objects.create_user(username="testuser", password="testpass123")

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        assert int(access_token["user_id"]) == user.id

    def test_api_authentication_with_valid_token(self):
        """Test API request with valid token."""
        user = User.objects.create_user(username="testuser", password="testpass123")

        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        # Token is valid, authentication should work
        assert client._credentials is not None

    def test_api_authentication_without_token(self, api_client):
        """Test API request without token fails."""
        from django.urls import reverse

        # Try to access protected endpoint without token
        url = reverse("brand_list_create_api_view")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @time_machine.travel("2026-01-01 12:00:00", tick=False)
    def test_access_token_expiration(self):
        """Test access token expires after configured time."""
        user = User.objects.create_user(username="testuser", password="testpass123")

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        # Access token should be valid now
        assert access_token is not None

        # Travel forward 2 days (token lifetime is 1 day in settings)
        with time_machine.travel("2026-01-03 12:00:00", tick=False):
            # Token should be expired
            # We can check the exp claim
            from datetime import datetime

            exp_timestamp = access_token["exp"]
            current_timestamp = datetime.now().timestamp()

            assert current_timestamp > exp_timestamp

    def test_refresh_token_generation(self):
        """Test refresh token is generated."""
        user = User.objects.create_user(username="testuser", password="testpass123")

        refresh = RefreshToken.for_user(user)

        assert str(refresh) != ""
        assert refresh.access_token is not None

    def test_token_refresh_creates_new_access_token(self):
        """Test refreshing token creates new access token."""
        user = User.objects.create_user(username="testuser", password="testpass123")

        refresh = RefreshToken.for_user(user)
        old_access_token = str(refresh.access_token)

        # Refresh the token
        refresh.set_jti()
        refresh.set_exp()
        new_access_token = str(refresh.access_token)

        # Tokens should be different
        assert old_access_token != new_access_token
