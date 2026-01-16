from django.urls import path

from suppliers import views

urlpatterns = [
    path(
        "suppliers/",
        views.SupplierListCreateAPIView.as_view(),
        name="supplier_list_create_api_view",
    ),
    path(
        "suppliers/<int:pk>/",
        views.SupplierRetrieveUpdateDestroyAPIView.as_view(),
        name="supplier_detail_api_view",
    ),
]
