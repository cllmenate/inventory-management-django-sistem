import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View

from app.services import metrics
from app.services.export_data import DataExportService
from app.services.import_data import DataImportService


@login_required(login_url="login")
def home(request):
    product_metrics = metrics.get_product_metrics()
    sales_metrics = metrics.get_sales_metrics()
    daily_sales_data = metrics.get_daily_sales_data()
    daily_sales_quantity_data = metrics.get_daily_sales_quantity_data()
    products_by_category = metrics.get_products_by_category()
    products_by_brand = metrics.get_products_by_brand()

    context = {
        "product_metrics": product_metrics,
        "sales_metrics": sales_metrics,
        "daily_sales_data": json.dumps(daily_sales_data),
        "daily_sales_quantity_data": json.dumps(daily_sales_quantity_data),
        "products_by_category": json.dumps(products_by_category),
        "products_by_brand": json.dumps(products_by_brand),
    }

    return render(request, "home.html", context)


def healthcheck(request):
    return JsonResponse({"status": "ok"})


class ExportView(LoginRequiredMixin, PermissionRequiredMixin, View):
    model = None
    filename = "export"
    template_name = None  # Needed for PDF

    def get(self, request, *args, **kwargs):
        file_format = request.GET.get("format", "csv")
        queryset = self.model.objects.all()
        # Optional: apply filters here if needed

        if file_format == "csv":
            return DataExportService.export_to_csv(queryset, self.filename)
        elif file_format == "json":
            return DataExportService.export_to_json(queryset, self.filename)
        elif file_format == "xml":
            return DataExportService.export_to_xml(queryset, self.filename)
        elif file_format == "pdf" and self.template_name:
            context = {self.model._meta.verbose_name_plural.lower(): queryset}
            return DataExportService.export_to_pdf(
                queryset, self.template_name, context, self.filename
            )
        else:
            messages.error(request, "Formato de exportação inválido.")
            return redirect(request.META.get("HTTP_REFERER", "/"))


class ImportView(LoginRequiredMixin, PermissionRequiredMixin, View):
    model = None
    success_url = None
    mapping_dict = None

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get("file")
        if not file_obj:
            messages.error(request, "Nenhum arquivo enviado.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        file_type = file_obj.name.split(".")[-1].lower()
        service = DataImportService(file_obj, file_type)

        try:
            count = service.transform_and_load(self.model, self.mapping_dict)
            messages.success(
                request, f"Importação concluída: {count} registros inseridos."
            )
        except Exception as e:
            messages.error(request, f"Erro na importação: {str(e)}")

        return redirect(self.success_url or request.META.get(
            "HTTP_REFERER", "/"
        ))
