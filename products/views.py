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

from app.services import metrics
from app.views import ExportView, ImportView
from categories.models import Category
from product_models.models import ProductModel
from products import forms, models, serializers

PERMISSIONS = [
    "products.view_product",
    "products.add_product",
    "products.change_product",
    "products.delete_product",
]


# Create your views here.
class ProductListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    model = models.Product
    template_name = "product_list.html"
    context_object_name = "products"
    paginate_by = 10
    permission_required = PERMISSIONS[0]

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get("title")
        serial_number = self.request.GET.get("serial_number")
        category = self.request.GET.get("category")
        product_model = self.request.GET.get("product_model")

        if title:
            queryset = queryset.filter(
                title__icontains=title
            )

        if serial_number:
            queryset = queryset.filter(
                serial_number__icontains=serial_number
            )

        if category:
            queryset = queryset.filter(
                category__id=category
            )

        if product_model:
            queryset = queryset.filter(
                product_model__id=product_model
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_metrics"] = metrics.get_product_metrics()
        context["categories"] = Category.objects.all()
        context["product_models"] = ProductModel.objects.all()
        return context


class ProductCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = models.Product
    template_name = "product_create.html"
    form_class = forms.ProductForm
    success_url = reverse_lazy("product_list")
    permission_required = PERMISSIONS[1]


class ProductDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView,
):
    model = models.Product
    template_name = "product_detail.html"
    permission_required = PERMISSIONS[0]


class ProductUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    model = models.Product
    template_name = "product_update.html"
    form_class = forms.ProductForm
    success_url = reverse_lazy("product_list")
    permission_required = PERMISSIONS[1]


class ProductDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    model = models.Product
    template_name = "product_delete.html"
    success_url = reverse_lazy("product_list")
    permission_required = PERMISSIONS[1]


class ProductExportView(ExportView):
    model = models.Product
    filename = "produtos"
    permission_required = PERMISSIONS[1]


class ProductImportView(ImportView):
    model = models.Product
    success_url = reverse_lazy("product_list")
    permission_required = PERMISSIONS[1]


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

    @extend_schema(
        tags=["Products"],
        summary="List and Create Products",
        description="List all products or create a new one.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=["Products"],
        summary="Create Product",
        description="Create a new product.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProductRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView,
):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

    @extend_schema(
        tags=["Products"],
        summary="Retrieve, Update or Destroy Product",
        description="Retrieve a product by ID, update it, or delete it.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=["Products"],
        summary="Update Product",
        description="Update a product by ID.",
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        tags=["Products"],
        summary="Partial Update Product",
        description="Partially update a product by ID.",
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        tags=["Products"],
        summary="Delete Product",
        description="Delete a product by ID.",
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
