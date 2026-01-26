from django.contrib import admin

from notifications.models import TaskNotification


@admin.register(TaskNotification)
class TaskNotificationAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "task_type",
        "model_name",
        "status",
        "created_at",
        "is_read",
    ]
    list_filter = ["task_type", "status", "is_read", "created_at"]
    search_fields = ["user__username", "model_name", "task_id"]
    readonly_fields = ["task_id", "created_at", "updated_at", "completed_at"]

    fieldsets = (
        (
            "Informações Básicas",
            {
                "fields": (
                    "user",
                    "task_type",
                    "task_id",
                    "status",
                )
            },
        ),
        (
            "Detalhes da Task",
            {
                "fields": (
                    "model_name",
                    "file_format",
                    "file_path",
                    "record_count",
                )
            },
        ),
        (
            "Resultado",
            {
                "fields": (
                    "error_message",
                )
            },
        ),
        (
            "Controle",
            {
                "fields": (
                    "is_read",
                    "created_at",
                    "updated_at",
                    "completed_at",
                )
            },
        ),
    )
