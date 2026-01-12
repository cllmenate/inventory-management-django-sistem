from rest_framework import generics
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
)
from django.urls import reverse_lazy
from inflows import models, forms, serializers


# Create your views here.
class InflowListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView
):
    model = models.Inflows
    template_name = 'inflow_list.html'
    context_object_name = 'inflows'
    paginate_by = 10
    permission_required = 'inflows.view_inflow'

    def get_queryset(self):
        queryset = super().get_queryset()
        product = (self.request.GET.get('product') or '').strip()
        serial_number = (self.request.GET.get('serial_number') or '').strip()
        category = self.request.GET.get('category')
        brand = self.request.GET.get('brand')

        if product:
            queryset = queryset.filter(product__title__icontains=product)
        if serial_number:
            queryset = queryset.filter(
                product__serial_number__icontains=serial_number
            )
        if category:
            queryset = queryset.filter(product__category__id=category)
        if brand:
            queryset = queryset.filter(product__brand__id=brand)

        return queryset


class InflowCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView
):
    model = models.Inflows
    template_name = 'inflow_create.html'
    form_class = forms.InflowForm
    success_url = reverse_lazy('inflow_list')
    permission_required = 'inflows.add_inflow'


class InflowDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView
):
    model = models.Inflows
    template_name = 'inflow_detail.html'
    permission_required = 'inflows.view_inflow'


class InflowListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Inflows.objects.all()
    serializer_class = serializers.InflowSerializer


class InflowRetrieveAPIView(generics.RetrieveAPIView):
    queryset = models.Inflows.objects.all()
    serializer_class = serializers.InflowSerializer
