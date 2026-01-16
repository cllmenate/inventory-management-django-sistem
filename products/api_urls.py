from django.urls import path

from products import views

urlpatterns = [
    path(
        "products/",
        views.ProductListCreateAPIView.as_view(),
        name="product_list_create_api_view",
    ),
    path(
        "products/<int:pk>/",
        views.ProductRetrieveUpdateDestroyAPIView.as_view(),
        name="product_detail_api_view",
    ),
]
