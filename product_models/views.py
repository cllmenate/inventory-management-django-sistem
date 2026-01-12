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
from product_models import models, forms, serializers
from brands.models import Brand


class ProductModelListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView
):
    model = models.ProductModel
    template_name = 'product_model_list.html'
    context_object_name = 'product_models'
    paginate_by = 10
    permission_required = 'product_models.view_product_model'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        brand = self.request.GET.get('brand')

        if name:
            queryset = queryset.filter(name__icontains=name)

        if brand:
            queryset = queryset.filter(brand__id=brand)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        return context


class ProductModelCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView
):
    model = models.ProductModel
    template_name = 'product_model_create.html'
    form_class = forms.ProductModelForm
    success_url = reverse_lazy('product_model_list')
    permission_required = 'product_models.add_product_model'


class ProductModelDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView
):
    model = models.ProductModel
    template_name = 'product_model_detail.html'
    permission_required = 'product_models.view_product_model'


class ProductModelUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView
):
    model = models.ProductModel
    template_name = 'product_model_update.html'
    form_class = forms.ProductModelForm
    success_url = reverse_lazy('product_model_list')
    permission_required = 'product_models.change_product_model'


class ProductModelDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView
):
    model = models.ProductModel
    template_name = 'product_model_delete.html'
    success_url = reverse_lazy('product_model_list')
    permission_required = 'product_models.delete_product_model'


class ProductModelListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.ProductModel.objects.all()
    serializer_class = serializers.ProductModelSerializer


class ProductModelRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = models.ProductModel.objects.all()
    serializer_class = serializers.ProductModelSerializer
