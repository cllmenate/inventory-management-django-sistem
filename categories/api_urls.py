from django.urls import path

from categories import views

urlpatterns = [
    path(
        "categories/",
        views.CategoryListCreateAPIView.as_view(),
        name="category_list_create_api_view",
    ),
    path(
        "categories/<int:pk>/",
        views.CategoryRetrieveUpdateDestroyAPIView.as_view(),
        name="category_detail_api_view",
    ),
]
