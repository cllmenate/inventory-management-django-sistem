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

from categories import forms, models, serializers


# Create your views here.
class CategoryListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    model = models.Category
    template_name = "category_list.html"
    context_object_name = "categories"
    paginate_by = 10
    permission_required = "categories.view_category"

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name")

        if name:
            queryset = queryset.filter(name__icontains=name)
            return queryset

        key = "categories_list_queryset"
        cached_qs = cache.get(key)

        if cached_qs:
            return cached_qs

        # Force evaluation to cache the result
        queryset = list(queryset)
        cache.set(key, queryset, 60 * 15)

        return queryset


class CategoryCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = models.Category
    template_name = "category_create.html"
    form_class = forms.CategoryForm
    success_url = reverse_lazy("category_list")
    permission_required = "categories.add_category"


class CategoryDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView,
):
    model = models.Category
    template_name = "category_detail.html"
    permission_required = "categories.view_category"


class CategoryUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    model = models.Category
    template_name = "category_update.html"
    form_class = forms.CategoryForm
    success_url = reverse_lazy("category_list")
    permission_required = "categories.change_category"


class CategoryDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    model = models.Category
    template_name = "category_delete.html"
    success_url = reverse_lazy("category_list")
    permission_required = "categories.delete_category"


class CategoryListCreateAPIView(
    generics.ListCreateAPIView,
):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

    @extend_schema(
        tags=["Categories"],
        summary="List and Create Categories",
        description="List all categories or create a new one.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=["Categories"],
        summary="Create Category",
        description="Create a new category.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CategoryRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView,
):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

    @extend_schema(
        tags=["Categories"],
        summary="Retrieve, Update or Destroy Category",
        description="Retrieve a category by ID, update it, or delete it.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=["Categories"],
        summary="Update Category",
        description="Update a category by ID.",
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        tags=["Categories"],
        summary="Partial Update Category",
        description="Partially update a category by ID.",
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        tags=["Categories"],
        summary="Delete Category",
        description="Delete a category by ID.",
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
