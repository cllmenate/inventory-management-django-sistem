"""Integration tests for API workflows."""

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.integration
@pytest.mark.api
@pytest.mark.django_db
class TestAPIIntegration:
    """Test suite for complete API workflows."""

    def test_complete_inventory_workflow_via_api(self, authenticated_client):
        """Test complete inventory management workflow via API."""
        # Step 1: Create a brand
        brand_url = reverse("brand_list_create_api_view")
        brand_data = {"name": "API Brand", "description": "Created via API"}
        brand_response = authenticated_client.post(brand_url, brand_data, format="json")
        assert brand_response.status_code == status.HTTP_201_CREATED
        brand_id = brand_response.data["id"]

        # Step 2: Create a category
        category_url = reverse("category_list_create_api_view")
        category_data = {"name": "API Category"}
        category_response = authenticated_client.post(
            category_url, category_data, format="json"
        )
        assert category_response.status_code == status.HTTP_201_CREATED
        category_id = category_response.data["id"]

        # Step 3: Create a product model
        product_model_url = reverse("product_model_list_create_api_view")
        product_model_data = {
            "name": "API Model",
            "brand": brand_id,
            "description": "Test model",
        }
        model_response = authenticated_client.post(
            product_model_url, product_model_data, format="json"
        )
        assert model_response.status_code == status.HTTP_201_CREATED
        product_model_id = model_response.data["id"]

        # Step 4: Create a product
        product_url = reverse("product_list_create_api_view")
        product_data = {
            "title": "API Product",
            "product_model": product_model_id,
            "category": category_id,
            "description": "Test product",
            "serial_number": "API123",
            "cost_price": "100.00",
            "sell_price": "150.00",
            "quantity": 0,
        }
        product_response = authenticated_client.post(
            product_url, product_data, format="json"
        )
        assert product_response.status_code == status.HTTP_201_CREATED
        product_id = product_response.data["id"]

        # Step 5: Create a supplier
        supplier_url = reverse("supplier_list_create_api_view")
        supplier_data = {"name": "API Supplier"}
        supplier_response = authenticated_client.post(
            supplier_url, supplier_data, format="json"
        )
        assert supplier_response.status_code == status.HTTP_201_CREATED
        supplier_id = supplier_response.data["id"]

        # Step 6: Create an inflow
        inflow_url = reverse("inflow_list_create_api_view")
        inflow_data = {
            "product": product_id,
            "supplier": supplier_id,
            "quantity": 100,
            "description": "Initial stock",
        }
        inflow_response = authenticated_client.post(
            inflow_url, inflow_data, format="json"
        )
        assert inflow_response.status_code == status.HTTP_201_CREATED

        # Step 7: Verify product quantity increased
        product_detail_url = reverse(
            "product_detail_api_view", kwargs={"pk": product_id}
        )
        product_check = authenticated_client.get(product_detail_url)
        assert product_check.data["quantity"] == 100

        # Step 8: Create an outflow
        outflow_url = reverse("outflow_list_create_api_view")
        outflow_data = {"product": product_id, "quantity": 30, "description": "Sale"}
        outflow_response = authenticated_client.post(
            outflow_url, outflow_data, format="json"
        )
        assert outflow_response.status_code == status.HTTP_201_CREATED

        # Step 9: Verify final quantity
        product_final = authenticated_client.get(product_detail_url)
        assert product_final.data["quantity"] == 70

    def test_api_authentication_flow(self, api_client):
        """Test API authentication is properly enforced."""
        # Without authentication, should fail
        url = reverse("brand_list_create_api_view")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # With authentication (using authenticated_client fixture would work)
        # This is tested in other test classes

    def test_api_crud_operations_on_brand(self, authenticated_client):
        """Test full CRUD via API for brands."""
        base_url = reverse("brand_list_create_api_view")

        # Create
        data = {"name": "CRUD Brand", "description": "Test"}
        create_response = authenticated_client.post(base_url, data, format="json")
        assert create_response.status_code == status.HTTP_201_CREATED
        brand_id = create_response.data["id"]

        # Read (List)
        list_response = authenticated_client.get(base_url)
        assert list_response.status_code == status.HTTP_200_OK
        assert any(b["id"] == brand_id for b in list_response.data)

        # Read (Detail)
        detail_url = reverse("brand_detail_api_view", kwargs={"pk": brand_id})
        detail_response = authenticated_client.get(detail_url)
        assert detail_response.status_code == status.HTTP_200_OK
        assert detail_response.data["name"] == "CRUD Brand"

        # Update
        update_data = {"name": "Updated Brand", "description": "Updated"}
        update_response = authenticated_client.put(
            detail_url, update_data, format="json"
        )
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.data["name"] == "Updated Brand"

        # Delete
        delete_response = authenticated_client.delete(detail_url)
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        # Verify deleted
        verify_response = authenticated_client.get(detail_url)
        assert verify_response.status_code == status.HTTP_404_NOT_FOUND
