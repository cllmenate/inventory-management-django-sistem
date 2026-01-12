from rest_framework import generics
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from products import models, forms, serializers
from app import metrics
from categories.models import Category
from product_models.models import ProductModel


# Create your views here.
class ProductListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView
):
    model = models.Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 10
    permission_required = 'products.view_product'

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get('title')
        serial_number = self.request.GET.get('serial_number')
        category = self.request.GET.get('category')
        product_model = self.request.GET.get('product_model')

        if title:
            queryset = queryset.filter(title__icontains=title)

        if serial_number:
            queryset = queryset.filter(serial_number__icontains=serial_number)

        if category:
            queryset = queryset.filter(category__id=category)

        if product_model:
            queryset = queryset.filter(product_model__id=product_model)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_metrics'] = metrics.get_product_metrics()
        context['categories'] = Category.objects.all()
        context['product_models'] = ProductModel.objects.all()
        return context


class ProductCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView
):
    model = models.Product
    template_name = 'product_create.html'
    form_class = forms.ProductForm
    success_url = reverse_lazy('product_list')
    permission_required = 'products.add_product'


class ProductDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView
):
    model = models.Product
    template_name = 'product_detail.html'
    permission_required = 'products.view_product'


class ProductUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView
):
    model = models.Product
    template_name = 'product_update.html'
    form_class = forms.ProductForm
    success_url = reverse_lazy('product_list')
    permission_required = 'products.change_product'


class ProductDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView
):
    model = models.Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'products.delete_product'


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer


class ProductRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
