from django.urls import path

from notifications import views

app_name = "notifications"

urlpatterns = [
    path(
        "",
        views.TaskNotificationListView.as_view(),
        name="notifications_list",
    ),
    path(
        "<int:notification_id>/download/",
        views.download_export,
        name="notifications_download",
    ),
    path(
        "<int:notification_id>/read/",
        views.mark_notification_read,
        name="notifications_mark_read",
    ),
]
