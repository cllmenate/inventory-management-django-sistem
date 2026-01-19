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

from app.views import ExportView, ImportView
from brands.models import Brand
from product_models import forms, models, serializers

PERMISSIONS = [
    "product_models.view_product_model",
    "product_models.add_product_model",
    "product_models.change_product_model",
    "product_models.delete_product_model",
]


class ProductModelListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    model = models.ProductModel
    template_name = "product_model_list.html"
    context_object_name = "product_models"
    paginate_by = 10
    permission_required = PERMISSIONS

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name")
        brand = self.request.GET.get("brand")

        if name:
            queryset = queryset.filter(name__icontains=name)

        if brand:
            queryset = queryset.filter(brand__id=brand)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["brands"] = Brand.objects.all()
        return context


class ProductModelCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = models.ProductModel
    template_name = "product_model_create.html"
    form_class = forms.ProductModelForm
    success_url = reverse_lazy("product_model_list")
    permission_required = PERMISSIONS


class ProductModelDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView,
):
    model = models.ProductModel
    template_name = "product_model_detail.html"
    permission_required = PERMISSIONS


class ProductModelUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    model = models.ProductModel
    template_name = "product_model_update.html"
    form_class = forms.ProductModelForm
    success_url = reverse_lazy("product_model_list")
    permission_required = PERMISSIONS


class ProductModelDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    model = models.ProductModel
    template_name = "product_model_delete.html"
    success_url = reverse_lazy("product_model_list")
    permission_required = PERMISSIONS


class ProductModelExportView(ExportView):
    model = models.ProductModel
    filename = "modelos-de-produto"
    permission_required = PERMISSIONS


class ProductModelImportView(ImportView):
    model = models.ProductModel
    success_url = reverse_lazy("product_model_list")
    permission_required = PERMISSIONS


class ProductModelListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.ProductModel.objects.all()
    serializer_class = serializers.ProductModelSerializer

    @extend_schema(
        tags=["Product Models"],
        summary="List and Create Product Models",
        description="List all product models or create a new one.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=["Product Models"],
        summary="Create Product Model",
        description="Create a new product model.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProductModelRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView,
):
    queryset = models.ProductModel.objects.all()
    serializer_class = serializers.ProductModelSerializer

    @extend_schema(
        tags=["Product Models"],
        summary="Retrieve, Update or Destroy Product Model",
        description="Retrieve a product model by ID, update it, or delete it.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=["Product Models"],
        summary="Update Product Model",
        description="Update a product model by ID.",
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        tags=["Product Models"],
        summary="Partial Update Product Model",
        description="Partially update a product model by ID.",
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        tags=["Product Models"],
        summary="Delete Product Model",
        description="Delete a product model by ID.",
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
