from django.urls import path

from inflows import views

urlpatterns = [
    path(
        "inflows/",
        views.InflowListCreateAPIView.as_view(),
        name="inflow_list_create_api_view",
    ),
    path(
        "inflows/<int:pk>/",
        views.InflowRetrieveAPIView.as_view(),
        name="inflow_detail_api_view",
    ),
]
