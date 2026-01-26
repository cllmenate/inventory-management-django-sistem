from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TaskNotification(models.Model):
    """Rastreia tarefas assíncronas de export/import."""

    TASK_TYPES = [
        ("export", "Exportação"),
        ("import", "Importação"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pendente"),
        ("processing", "Processando"),
        ("completed", "Concluído"),
        ("failed", "Falhou"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="task_notifications",
    )
    task_type = models.CharField(
        max_length=10,
        choices=TASK_TYPES,
    )
    task_id = models.CharField(
        max_length=255,
        unique=True,
    )  # Celery task ID
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    # Metadados
    model_name = models.CharField(max_length=100)
    file_format = models.CharField(max_length=10, blank=True)  # Para exports
    file_path = models.FileField(
        upload_to="exports/%Y/%m/%d/",
        blank=True,
        null=True,
    )

    # Resultados
    record_count = models.IntegerField(
        null=True,
        blank=True,
    )
    error_message = models.TextField(
        blank=True,
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    # Controle de lidos
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "is_read"]),
            models.Index(fields=["task_id"]),
        ]

    def __str__(self):
        return f"{self.get_task_type_display()} - {self.model_name} ({self.status})"  # noqa: E501
