from django.urls import path

from brands import views

urlpatterns = [
    path(
        "brands/",
        views.BrandListCreateAPIView.as_view(),
        name="brand_list_create_api_view",
    ),
    path(
        "brands/<int:pk>/",
        views.BrandRetrieveUpdateDestroyAPIView.as_view(),
        name="brand_detail_api_view",
    ),
]
