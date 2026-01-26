from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView

from notifications.models import TaskNotification


class TaskNotificationListView(LoginRequiredMixin, ListView):
    model = TaskNotification
    template_name = "notifications/task_list.html"
    context_object_name = "notifications"
    paginate_by = 20

    def get_queryset(self):
        return TaskNotification.objects.filter(user=self.request.user)


@login_required
def download_export(request, notification_id):
    """Faz download de arquivo exportado."""
    notification = get_object_or_404(
        TaskNotification,
        id=notification_id,
        user=request.user,
        task_type="export",
    )

    if not notification.file_path:
        raise Http404("Arquivo não encontrado")

    # Marcar como lido
    notification.is_read = True
    notification.save()

    return FileResponse(
        notification.file_path.open("rb"),
        as_attachment=True,
        filename=notification.file_path.name.split("/")[-1],
    )


@login_required
def mark_notification_read(request, notification_id):
    """Marca notificação como lida."""
    notification = get_object_or_404(
        TaskNotification, id=notification_id, user=request.user
    )
    notification.is_read = True
    notification.save()
    return redirect(request.META.get("HTTP_REFERER", "/"))
