import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestAppViews:
    def test_home_view_authenticated(self, client, authenticated_user):
        client.force_login(authenticated_user)
        url = reverse("home")
        response = client.get(url)
        assert response.status_code == 200
        # Check context contains metrics keys
        assert "product_metrics" in response.context
        assert "sales_metrics" in response.context

    def test_home_view_anonymous(self, client):
        url = reverse("home")
        response = client.get(url)
        # Should redirect to login
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_healthcheck(self, client):
        url = reverse("healthcheck")
        response = client.get(url)
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
