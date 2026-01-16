from django.urls import path

from product_models import views

urlpatterns = [
    path(
        "products/models/",
        views.ProductModelListCreateAPIView.as_view(),
        name="product_model_list_create_api_view",
    ),
    path(
        "products/models/<int:pk>/",
        views.ProductModelRetrieveUpdateDestroyAPIView.as_view(),
        name="product_model_detail_api_view",
    ),
]
