import pytest  # noqa: F401
from django.urls import resolve, reverse

from notifications import views


class TestNotificationURLs:
    def test_list_url(self):
        url = reverse("notifications:notifications_list")
        assert resolve(url).func.view_class == views.TaskNotificationListView

    def test_download_url(self):
        url = reverse(
            "notifications:notifications_download",
            kwargs={"notification_id": 1}
        )
        assert resolve(url).func == views.download_export

    def test_mark_read_url(self):
        url = reverse(
            "notifications:notifications_mark_read",
            kwargs={"notification_id": 1}
        )
        assert resolve(url).func == views.mark_notification_read
