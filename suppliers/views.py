from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from drf_spectacular.utils import extend_schema
from rest_framework import generics

from suppliers import forms, models, serializers


# Create your views here.
class SupplierListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    model = models.Supplier
    template_name = "supplier_list.html"
    context_object_name = "suppliers"
    paginate_by = 10
    permission_required = "suppliers.view_supplier"

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name")

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class SupplierCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = models.Supplier
    template_name = "supplier_create.html"
    form_class = forms.SupplierForm
    success_url = reverse_lazy("supplier_list")
    permission_required = "suppliers.add_supplier"


class SupplierDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView,
):
    model = models.Supplier
    template_name = "supplier_detail.html"
    permission_required = "suppliers.view_supplier"


class SupplierUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    model = models.Supplier
    template_name = "supplier_update.html"
    form_class = forms.SupplierForm
    success_url = reverse_lazy("supplier_list")
    permission_required = "suppliers.add_supplier"


class SupplierDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    model = models.Supplier
    template_name = "supplier_delete.html"
    success_url = reverse_lazy("supplier_list")
    permission_required = "suppliers.delete_supplier"


class SupplierListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Supplier.objects.all()
    serializer_class = serializers.SupplierSerializer

    @extend_schema(
        tags=["Suppliers"],
        summary="List and Create Suppliers",
        description="List all suppliers or create a new one.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=["Suppliers"],
        summary="Create Supplier",
        description="Create a new supplier.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class SupplierRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView,
):
    queryset = models.Supplier.objects.all()
    serializer_class = serializers.SupplierSerializer

    @extend_schema(
        tags=["Suppliers"],
        summary="Retrieve, Update or Destroy Supplier",
        description="Retrieve a supplier by ID, update it, or delete it.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=["Suppliers"],
        summary="Update Supplier",
        description="Update a supplier by ID.",
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        tags=["Suppliers"],
        summary="Partial Update Supplier",
        description="Partially update a supplier by ID.",
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        tags=["Suppliers"],
        summary="Delete Supplier",
        description="Delete a supplier by ID.",
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
