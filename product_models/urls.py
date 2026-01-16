from django.urls import path

from product_models import views

urlpatterns = [
    path(
        "products/models/list/",
        views.ProductModelListView.as_view(),
        name="product_model_list",
    ),
    path(
        "products/models/create/",
        views.ProductModelCreateView.as_view(),
        name="product_model_create",
    ),
    path(
        "products/models/<int:pk>/detail/",
        views.ProductModelDetailView.as_view(),
        name="product_model_detail",
    ),
    path(
        "products/models/<int:pk>/update/",
        views.ProductModelUpdateView.as_view(),
        name="product_model_update",
    ),
    path(
        "products/models/<int:pk>/delete/",
        views.ProductModelDeleteView.as_view(),
        name="product_model_delete",
    ),
]
