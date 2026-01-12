"""Tests for Brand views."""

import pytest
from django.urls import reverse
from django.contrib.auth.models import Permission
from brands.models import Brand
from tests.factories import BrandFactory, UserFactory


@pytest.mark.django_db
class TestBrandListView:
    """Test suite for BrandListView."""

    def test_brand_list_view_requires_authentication(self, client):
        """Test view requires authentication."""
        url = reverse("brand_list")
        response = client.get(url)

        assert response.status_code == 302
        assert "/login/" in response.url

    def test_brand_list_view_with_authenticated_user(self, client, authenticated_user):
        """Test view with authenticated user."""
        client.force_login(authenticated_user)
        url = reverse("brand_list")
        response = client.get(url)

        assert response.status_code == 200
        assert "brands" in response.context

    def test_brand_list_view_shows_all_brands(
        self, client, authenticated_user, brand_list
    ):
        """Test view shows all brands."""
        client.force_login(authenticated_user)
        url = reverse("brand_list")
        response = client.get(url)

        assert response.status_code == 200
        assert len(response.context["brands"]) == 5

    def test_brand_list_view_search_by_name(self, client, authenticated_user):
        """Test search functionality."""
        BrandFactory(name="Nike")
        BrandFactory(name="Adidas")
        BrandFactory(name="Puma")

        client.force_login(authenticated_user)
        url = reverse("brand_list") + "?name=Nike"
        response = client.get(url)

        assert response.status_code == 200
        brands = list(response.context["brands"])
        assert len(brands) == 1
        assert brands[0].name == "Nike"

    def test_brand_list_view_pagination(self, client, authenticated_user):
        """Test pagination works correctly."""
        BrandFactory.create_batch(15)

        client.force_login(authenticated_user)
        url = reverse("brand_list")
        response = client.get(url)

        assert response.status_code == 200
        assert len(response.context["brands"]) == 10  # paginate_by = 10


@pytest.mark.django_db
class TestBrandCreateView:
    """Test suite for BrandCreateView."""

    def test_brand_create_view_requires_permission(
        self, client, user_without_permissions
    ):
        """Test view requires add_brand permission."""
        client.force_login(user_without_permissions)
        url = reverse("brand_create")
        response = client.get(url)

        assert response.status_code == 403

    def test_brand_create_view_with_permission(self, client, authenticated_user):
        """Test view with proper permission."""
        client.force_login(authenticated_user)
        url = reverse("brand_create")
        response = client.get(url)

        assert response.status_code == 200

    def test_brand_create_post_valid_data(self, client, authenticated_user):
        """Test creating brand with valid data."""
        client.force_login(authenticated_user)
        url = reverse("brand_create")
        data = {"name": "New Brand", "description": "New Description"}
        response = client.post(url, data)

        assert response.status_code == 302
        assert Brand.objects.filter(name="New Brand").exists()


@pytest.mark.django_db
class TestBrandDetailView:
    """Test suite for BrandDetailView."""

    def test_brand_detail_view(self, client, authenticated_user, brand):
        """Test brand detail view."""
        client.force_login(authenticated_user)
        url = reverse("brand_detail", kwargs={"pk": brand.pk})
        response = client.get(url)

        assert response.status_code == 200
        assert response.context["brand"] == brand


@pytest.mark.django_db
class TestBrandUpdateView:
    """Test suite for BrandUpdateView."""

    def test_brand_update_view_requires_permission(
        self, client, user_without_permissions, brand
    ):
        """Test view requires change_brand permission."""
        client.force_login(user_without_permissions)
        url = reverse("brand_update", kwargs={"pk": brand.pk})
        response = client.get(url)

        assert response.status_code == 403

    def test_brand_update_post_valid_data(self, client, authenticated_user, brand):
        """Test updating brand with valid data."""
        client.force_login(authenticated_user)
        url = reverse("brand_update", kwargs={"pk": brand.pk})
        data = {"name": "Updated Brand", "description": "Updated Description"}
        response = client.post(url, data)

        assert response.status_code == 302
        brand.refresh_from_db()
        assert brand.name == "Updated Brand"
        assert brand.description == "Updated Description"


@pytest.mark.django_db
class TestBrandDeleteView:
    """Test suite for BrandDeleteView."""

    def test_brand_delete_view_requires_permission(
        self, client, user_without_permissions, brand
    ):
        """Test view requires delete_brand permission."""
        client.force_login(user_without_permissions)
        url = reverse("brand_delete", kwargs={"pk": brand.pk})
        response = client.get(url)

        assert response.status_code == 403

    def test_brand_delete_post(self, client, authenticated_user, brand):
        """Test deleting brand."""
        client.force_login(authenticated_user)
        brand_id = brand.id
        url = reverse("brand_delete", kwargs={"pk": brand.pk})
        response = client.post(url)

        assert response.status_code == 302
        assert not Brand.objects.filter(id=brand_id).exists()
