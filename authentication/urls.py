from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from authentication.views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
)

urlpatterns = [
    path(
        "authentication/token/",
        CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "authentication/token/refresh/",
        CustomTokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "authentication/token/verify/", TokenVerifyView.as_view(), name="token_verify"
    ),
]
