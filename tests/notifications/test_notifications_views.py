import pytest
from django.core.files.base import ContentFile
from django.urls import reverse

from notifications.models import TaskNotification


@pytest.mark.django_db
class TestNotificationViews:
    def test_notification_list_view(self, client, authenticated_user):
        client.force_login(authenticated_user)
        # Create a notification for this user
        TaskNotification.objects.create(
            user=authenticated_user,
            task_type="export",
            task_id="123",
            model_name="Brand",
        )
        url = reverse("notifications:notifications_list")
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.context["notifications"]) == 1

    def test_notification_mark_read(self, client, authenticated_user):
        client.force_login(authenticated_user)
        notification = TaskNotification.objects.create(
            user=authenticated_user,
            task_type="import",
            task_id="456",
            model_name="Brand",
            is_read=False,
        )
        url = reverse(
            "notifications:notifications_mark_read",
            kwargs={"notification_id": notification.id},
        )
        response = client.get(url, HTTP_REFERER="/previous/")
        assert response.status_code == 302
        notification.refresh_from_db()
        assert notification.is_read is True

    def test_notification_download(self, client, authenticated_user):
        client.force_login(authenticated_user)

        notification = TaskNotification(
            user=authenticated_user,
            task_type="export",
            task_id="789",
            model_name="Brand",
        )
        # Use ContentFile to ensure file is saved in valid storage
        notification.file_path.save("export.csv", ContentFile(b"content"))
        notification.save()

        url = reverse(
            "notifications:notifications_download",
            kwargs={"notification_id": notification.id},
        )
        response = client.get(url)
        assert response.status_code == 200
        assert "export" in response["Content-Disposition"]
        assert ".csv" in response["Content-Disposition"]

        # Should mark as read after download
        notification.refresh_from_db()
        assert notification.is_read is True
