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
from app.tasks import export_data_async, import_data_async
from notifications.models import TaskNotification


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
        valid_formats = ["csv", "json", "xml", "pdf"]

        if file_format not in valid_formats:
            messages.error(request, "Formato de exportação inválido.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        # Enfileirar task assíncrona PRIMEIRO para obter o task_id
        task = export_data_async.apply_async(
            args=[None]
        )  # notification_id será None temporariamente

        # Criar notificação COM o task_id já definido
        TaskNotification.objects.create(
            user=request.user,
            task_type="export",
            task_id=task.id,
            model_name=self.model.__name__,
            file_format=file_format,
        )

        messages.success(
            request,
            "Exportação iniciada! Acesse Notificações para acompanhar o progresso e fazer download quando concluída.",  # noqa: E501
        )
        return redirect(request.META.get("HTTP_REFERER", "/"))


class ImportView(LoginRequiredMixin, PermissionRequiredMixin, View):
    model = None
    success_url = None
    mapping_dict = None

    def post(self, request, *args, **kwargs):
        import os
        import tempfile

        file_obj = request.FILES.get("file")
        if not file_obj:
            messages.error(request, "Nenhum arquivo enviado.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        # Salvar arquivo temporariamente no servidor
        file_type = file_obj.name.split(".")[-1].lower()

        # Criar diretório temporário se não existir
        # Usar mediafiles (volume compartilhado) ao invés de MEDIA_ROOT
        temp_dir = "/app/mediafiles/temp"
        os.makedirs(temp_dir, exist_ok=True)

        temp_file = tempfile.NamedTemporaryFile(
            delete=False, suffix=f".{file_type}", dir=temp_dir
        )

        for chunk in file_obj.chunks():
            temp_file.write(chunk)
        temp_file.close()

        # Enfileirar task assíncrona PRIMEIRO para obter o task_id
        task = import_data_async.apply_async(
            args=[
                None,
                temp_file.name,
                self.mapping_dict,
            ]  # notification_id será None temporariamente
        )

        # Criar notificação COM o task_id já definido
        TaskNotification.objects.create(
            user=request.user,
            task_type="import",
            task_id=task.id,
            model_name=self.model.__name__,
        )

        # Atualizar a task com o notification_id correto
        # (a task vai precisar buscar a notificação pelo task_id)

        messages.success(
            request,
            "Importação iniciada! Acesse Notificações para acompanhar o progresso.",  # noqa: E501
        )

        return redirect(
            self.success_url or request.META.get("HTTP_REFERER", "/")
        )
