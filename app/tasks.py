import logging
import os

from celery import shared_task
from django.apps import apps
from django.core.cache import cache
from django.core.files.base import ContentFile
from django.utils import timezone

from app.services import metrics
from app.services.export_data import DataExportService
from app.services.import_data import DataImportService
from notifications.models import TaskNotification


@shared_task(bind=True, name="app.tasks.export_data_async")
def export_data_async(self, notification_id):
    """Exporta dados e salva arquivo para download."""
    try:
        # Buscar notificação pelo task_id se notification_id for None
        if notification_id is None:
            notification = TaskNotification.objects.get(
                task_id=self.request.id
            )
        else:
            notification = TaskNotification.objects.get(
                id=notification_id
            )

        notification.status = "processing"
        notification.save()

        # Obter modelo dinamicamente
        # Formato esperado: "app_label.ModelName" ou apenas "ModelName"
        if "." in notification.model_name:
            app_label, model_name = notification.model_name.split(".", 1)
        else:
            # Tentar inferir app_label pelo nome do modelo
            model_name = notification.model_name
            # Mapeamento common (pode ser melhorado)
            model_to_app = {
                "Product": "products",
                "Brand": "brands",
                "Category": "categories",
                "Supplier": "suppliers",
                "ProductModel": "product_models",
                "Inflows": "inflows",
                "Outflows": "outflows",
            }
            app_label = model_to_app.get(model_name)
            if not app_label:
                raise ValueError(
                    f"App não encontrado para o modelo: {model_name}"
                )

        model_class = apps.get_model(app_label, model_name)
        queryset = model_class.objects.all()

        # Gerar arquivo
        file_format = notification.file_format
        timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{model_name.lower()}_{timestamp}"

        # Gerar conteúdo baseado no formato
        if file_format == "csv":
            response = DataExportService.export_to_csv(queryset, filename)
        elif file_format == "json":
            response = DataExportService.export_to_json(queryset, filename)
        elif file_format == "xml":
            response = DataExportService.export_to_xml(queryset, filename)
        elif file_format == "pdf":
            context = {
                "queryset": queryset,
                "model_name": model_class._meta.verbose_name,
            }
            response = DataExportService.export_to_pdf(
                queryset, "generic_list_pdf.html", context, filename
            )
        else:
            raise ValueError(f"Formato não suportado: {file_format}")

        # Salvar arquivo
        file_name = f"{filename}.{file_format}"
        notification.file_path.save(
            file_name, ContentFile(response.content), save=False
        )
        notification.record_count = queryset.count()
        notification.status = "completed"
        notification.completed_at = timezone.now()
        notification.save()

        return {"status": "success", "count": queryset.count()}

    except Exception as e:
        notification.status = "failed"
        notification.error_message = str(e)
        notification.completed_at = timezone.now()
        notification.save()
        raise


@shared_task(bind=True, name="app.tasks.import_data_async")
def import_data_async(self, notification_id, file_path, mapping_dict=None):
    """Importa dados de arquivo."""
    try:
        # Buscar notificação pelo task_id se notification_id for None
        if notification_id is None:
            notification = TaskNotification.objects.get(
                task_id=self.request.id
            )
        else:
            notification = TaskNotification.objects.get(
                id=notification_id
            )

        notification.status = "processing"
        notification.save()

        # Obter modelo
        if "." in notification.model_name:
            app_label, model_name = notification.model_name.split(".", 1)
        else:
            model_name = notification.model_name
            model_to_app = {
                "Product": "products",
                "Brand": "brands",
                "Category": "categories",
                "Supplier": "suppliers",
                "ProductModel": "product_models",
                "Inflows": "inflows",
                "Outflows": "outflows",
            }
            app_label = model_to_app.get(model_name)
            if not app_label:
                raise ValueError(
                    f"App não encontrado para o modelo: {model_name}"
                )

        model_class = apps.get_model(app_label, model_name)

        # Detectar tipo
        file_type = file_path.split(".")[-1].lower()

        # Importar
        with open(file_path, "rb") as f:
            service = DataImportService(f, file_type)
            count = service.transform_and_load(model_class, mapping_dict)

        # Limpar arquivo temporário
        os.remove(file_path)

        # Atualizar notificação
        notification.record_count = count
        notification.status = "completed"
        notification.completed_at = timezone.now()
        notification.save()

        return {"status": "success", "count": count}

    except Exception as e:
        try:
            os.remove(file_path)
        except:  # noqa: E722
            logging.error("Erro ao remover arquivo temporário: %s", file_path)
            raise

        notification.status = "failed"
        notification.error_message = str(e)
        notification.completed_at = timezone.now()
        notification.save()
        raise


@shared_task(name="app.tasks.update_dashboard_metrics_cache")
def update_dashboard_metrics_cache():
    """Atualiza cache de métricas do dashboard periodicamente."""
    try:
        # Cache TTL de 10 minutos (2x o intervalo do beat para segurança)
        cache_ttl = 60 * 10

        # Atualizar cada métrica no cache
        cache.set(
            "metrics:product",
            metrics.get_product_metrics_raw(),
            cache_ttl,
        )
        cache.set(
            "metrics:sales",
            metrics.get_sales_metrics_raw(),
            cache_ttl,
        )
        cache.set(
            "metrics:daily_sales",
            metrics.get_daily_sales_data_raw(),
            cache_ttl,
        )
        cache.set(
            "metrics:daily_sales_quantity",
            metrics.get_daily_sales_quantity_data_raw(),
            cache_ttl,
        )
        cache.set(
            "metrics:products_by_category",
            metrics.get_products_by_category_raw(),
            cache_ttl,
        )
        cache.set(
            "metrics:products_by_brand",
            metrics.get_products_by_brand_raw(),
            cache_ttl,
        )

        return {
            "status": "success",
            "updated_at": timezone.now().isoformat(),
        }

    except Exception as e:
        logging.error(f"Erro ao atualizar cache de métricas: {e}")
        raise
