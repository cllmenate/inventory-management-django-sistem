from authentication.views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
)


class TestAuthenticationViews:
    def test_custom_token_obtain_pair_view_throttle(self):
        view = CustomTokenObtainPairView()
        assert view.throttle_scope == "auth"

    def test_custom_token_refresh_view_throttle(self):
        view = CustomTokenRefreshView()
        assert view.throttle_scope == "auth"
