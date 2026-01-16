from django.urls import path

from outflows import views

urlpatterns = [
    path(
        "outflows/",
        views.OutflowListCreateAPIView.as_view(),
        name="outflow_list_create_api_view",
    ),
    path(
        "outflows/<int:pk>/",
        views.OutflowRetrieveAPIView.as_view(),
        name="outflow_detail_api_view",
    ),
]
