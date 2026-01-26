import pytest  # noqa: F401
from django.urls import resolve, reverse
from rest_framework_simplejwt.views import TokenVerifyView

from authentication.views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
)


class TestAuthenticationURLs:
    def test_token_obtain_pair_url(self):
        url = reverse("token_obtain_pair")
        assert resolve(url).func.view_class == CustomTokenObtainPairView

    def test_token_refresh_url(self):
        url = reverse("token_refresh")
        assert resolve(url).func.view_class == CustomTokenRefreshView

    def test_token_verify_url(self):
        url = reverse("token_verify")
        assert resolve(url).func.view_class == TokenVerifyView
