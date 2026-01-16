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

from app import metrics
from outflows import forms, models, serializers


# Create your views here.
class OutflowListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Outflows
    template_name = "outflow_list.html"
    context_object_name = "outflows"
    paginate_by = 10
    permission_required = "outflows.view_outflow"

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
        context["sales_metrics"] = metrics.get_sales_metrics()

        return context


class OutflowCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = models.Outflows
    template_name = "outflow_create.html"
    form_class = forms.OutflowForm
    success_url = reverse_lazy("outflow_list")
    permission_required = "outflows.add_outflow"


class OutflowDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView,
):
    model = models.Outflows
    template_name = "outflow_detail.html"
    permission_required = "outflows.view_outflow"


class OutflowListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Outflows.objects.all()
    serializer_class = serializers.OutflowSerializer

    @extend_schema(
        tags=["Outflows"],
        summary="List and Create Outflows",
        description="List all outflows or create a new one.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=["Outflows"],
        summary="Create Outflow",
        description="Create a new outflow.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class OutflowRetrieveAPIView(generics.RetrieveAPIView):
    queryset = models.Outflows.objects.all()
    serializer_class = serializers.OutflowSerializer

    @extend_schema(
        tags=["Outflows"],
        summary="Retrieve Outflow",
        description="Retrieve an outflow by ID.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
