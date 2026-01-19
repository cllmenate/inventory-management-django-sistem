from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.core.cache import cache
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

from app.views import ExportView, ImportView
from brands import forms, models, serializers

PERMISSIONS = [
    "brands.view_brand",
    "brands.add_brand",
    "brands.change_brand",
    "brands.delete_brand",
]


# Create your views here.
class BrandListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Brand
    template_name = "brand_list.html"
    context_object_name = "brands"
    paginate_by = 10
    permission_required = PERMISSIONS

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name")

        if name:
            queryset = queryset.filter(name__icontains=name)
            return queryset

        key = "brands_list_queryset"
        cached_qs = cache.get(key)

        if cached_qs:
            return cached_qs

        # Force evaluation to cache the result
        queryset = list(queryset)
        cache.set(key, queryset, 60 * 15)

        return queryset


class BrandCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Brand
    template_name = "brand_create.html"
    form_class = forms.BrandForm
    success_url = reverse_lazy("brand_list")
    permission_required = PERMISSIONS


class BrandDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Brand
    template_name = "brand_detail.html"
    permission_required = PERMISSIONS


class BrandUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Brand
    template_name = "brand_update.html"
    form_class = forms.BrandForm
    success_url = reverse_lazy("brand_list")
    permission_required = PERMISSIONS


class BrandDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Brand
    template_name = "brand_delete.html"
    success_url = reverse_lazy("brand_list")
    permission_required = PERMISSIONS


class BrandExportView(ExportView):
    model = models.Brand
    filename = "marcas"
    permission_required = PERMISSIONS


class BrandImportView(ImportView):
    model = models.Brand
    success_url = reverse_lazy("brand_list")
    permission_required = PERMISSIONS


class BrandListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer

    @extend_schema(
        tags=["Brands"],
        summary="List and Create Brands",
        description="List all brands or create a new one.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=["Brands"],
        summary="Create Brand",
        description="Create a new brand.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class BrandRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer

    @extend_schema(
        tags=["Brands"],
        summary="Retrieve, Update or Destroy Brand",
        description="Retrieve a brand by ID, update it, or delete it.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=["Brands"],
        summary="Update Brand",
        description="Update a brand by ID.",
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        tags=["Brands"],
        summary="Partial Update Brand",
        description="Partially update a brand by ID.",
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        tags=["Brands"],
        summary="Delete Brand",
        description="Delete a brand by ID.",
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
