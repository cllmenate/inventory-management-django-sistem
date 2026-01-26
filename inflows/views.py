from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
)
from drf_spectacular.utils import extend_schema
from rest_framework import generics

from app.services import metrics
from app.views import ExportView, ImportView
from brands.models import Brand
from categories.models import Category
from inflows import forms, models, serializers

PERMISSIONS = [
    "inflows.view_inflows",
    "inflows.add_inflows",
]


# Create your views here.
class InflowListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    model = models.Inflows
    template_name = "inflow_list.html"
    context_object_name = "inflows"
    paginate_by = 10
    permission_required = PERMISSIONS[0]

    def get_queryset(self):
        queryset = super().get_queryset()
        product = (self.request.GET.get("product") or "").strip()
        serial_number = (self.request.GET.get("serial_number") or "").strip()
        category = self.request.GET.get("category")
        brand = self.request.GET.get("brand")

        if product:
            queryset = queryset.filter(
                product__title__icontains=product
            )
        if serial_number:
            queryset = queryset.filter(
                product__serial_number__icontains=serial_number
            )
        if category:
            queryset = queryset.filter(
                product__category__id=category
            )
        if brand:
            queryset = queryset.filter(
                product__brand__id=brand
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_metrics"] = metrics.get_product_metrics()
        context["categories"] = Category.objects.all()
        context["brands"] = Brand.objects.all()

        return context


class InflowCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = models.Inflows
    template_name = "inflow_create.html"
    form_class = forms.InflowForm
    success_url = reverse_lazy("inflow_list")
    permission_required = PERMISSIONS[1]


class InflowDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView,
):
    model = models.Inflows
    template_name = "inflow_detail.html"
    permission_required = PERMISSIONS[0]


class InflowExportView(ExportView):
    model = models.Inflows
    filename = "inflows"
    template_name = "inflow_list.html"
    permission_required = PERMISSIONS[1]


class InflowImportView(ImportView):
    model = models.Inflows
    success_url = reverse_lazy("inflow_list")
    permission_required = PERMISSIONS[1]


class InflowListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Inflows.objects.all()
    serializer_class = serializers.InflowSerializer

    @extend_schema(
        tags=["Inflows"],
        summary="List and Create Inflows",
        description="List all inflows or create a new one.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=["Inflows"],
        summary="Create Inflow",
        description="Create a new inflow.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class InflowRetrieveAPIView(generics.RetrieveAPIView):
    queryset = models.Inflows.objects.all()
    serializer_class = serializers.InflowSerializer

    @extend_schema(
        tags=["Inflows"],
        summary="Retrieve Inflow",
        description="Retrieve an inflow by ID.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
