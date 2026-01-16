from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from app import views

API_PATH = "api/v1/"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/",
         auth_views.LoginView.as_view(),
         name="login"),
    path("logout/",
         auth_views.LogoutView.as_view(),
         name="logout"),
    path(
        API_PATH + "schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        API_PATH + "docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        API_PATH + "redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path(API_PATH, include("authentication.urls")),
    path("health/", views.healthcheck, name="healthcheck"),
    path("", views.home, name="home"),
    # Template URLs
    path("", include("brands.urls")),
    path("", include("categories.urls")),
    path("", include("suppliers.urls")),
    path("", include("product_models.urls")),
    path("", include("products.urls")),
    path("", include("inflows.urls")),
    path("", include("outflows.urls")),
    # API URLs
    path(API_PATH, include("brands.api_urls")),
    path(API_PATH, include("categories.api_urls")),
    path(API_PATH, include("suppliers.api_urls")),
    path(API_PATH, include("product_models.api_urls")),
    path(API_PATH, include("products.api_urls")),
    path(API_PATH, include("inflows.api_urls")),
    path(API_PATH, include("outflows.api_urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
