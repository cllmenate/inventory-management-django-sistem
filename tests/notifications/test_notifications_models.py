import pytest  # noqa: F401

from notifications.models import TaskNotification


@pytest.mark.django_db
class TestNotificationModels:
    def test_notification_str(self, authenticated_user):
        notification = TaskNotification.objects.create(
            user=authenticated_user,
            task_type="export",
            task_id="123",
            model_name="Brand",
        )
        assert str(notification) == "Exportação - Brand (pending)"
