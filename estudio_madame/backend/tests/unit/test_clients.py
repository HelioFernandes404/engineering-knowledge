"""
Unit tests for Clients endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from uuid import uuid4

from app.models.client import Client


@pytest.mark.unit
class TestListClients:
    """Tests for GET /api/v1/clients"""

    def test_list_clients_success(
        self,
        client: TestClient,
        auth_headers: dict,
        test_client_model: Client
    ):
        """Test listing all clients"""
        response = client.get(
            "/api/v1/clients",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "meta" in data
        assert isinstance(data["data"], list)
        assert len(data["data"]) >= 1

    def test_list_clients_with_pagination(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test client pagination"""
        response = client.get(
            "/api/v1/clients?page=1&limit=20",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["meta"]["page"] == 1
        assert data["meta"]["limit"] == 20

    def test_list_clients_search_by_name(
        self,
        client: TestClient,
        auth_headers: dict,
        test_client_model: Client
    ):
        """Test searching clients by name"""
        response = client.get(
            "/api/v1/clients?search=John",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) >= 1

    def test_list_clients_search_by_email(
        self,
        client: TestClient,
        auth_headers: dict,
        test_client_model: Client
    ):
        """Test searching clients by email"""
        response = client.get(
            "/api/v1/clients?search=john@example.com",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) >= 1

    def test_list_clients_unauthorized(self, client: TestClient):
        """Test listing clients without authentication"""
        response = client.get("/api/v1/clients")

        assert response.status_code == 401


@pytest.mark.unit
class TestCreateClient:
    """Tests for POST /api/v1/clients"""

    def test_create_client_success(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test creating a new client"""
        response = client.post(
            "/api/v1/clients",
            headers=auth_headers,
            json={
                "name": "Jane Smith",
                "email": "jane.smith@example.com",
                "password": "securepassword",
                "phone": "+1987654321"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["data"]["name"] == "Jane Smith"
        assert data["data"]["email"] == "jane.smith@example.com"
        assert "id" in data["data"]

    def test_create_client_minimal_fields(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test creating client with only required fields"""
        response = client.post(
            "/api/v1/clients",
            headers=auth_headers,
            json={
                "name": "Minimal Client",
                "email": "minimal@example.com",
                "password": "password"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["data"]["name"] == "Minimal Client"

    def test_create_client_with_avatar(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test creating client with avatar"""
        response = client.post(
            "/api/v1/clients",
            headers=auth_headers,
            json={
                "name": "Avatar Client",
                "email": "avatar@example.com",
                "avatar": "https://example.com/avatar.jpg",
                "password": "password"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["data"]["avatar"] == "https://example.com/avatar.jpg"

    def test_create_client_missing_required_fields(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test creating client without required fields"""
        response = client.post(
            "/api/v1/clients",
            headers=auth_headers,
            json={"name": "No Email"}
        )

        assert response.status_code == 422

    def test_create_client_invalid_email(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test creating client with invalid email format"""
        response = client.post(
            "/api/v1/clients",
            headers=auth_headers,
            json={
                "name": "Invalid Email",
                "email": "not-an-email"
            }
        )

        assert response.status_code == 422

    def test_create_client_duplicate_email(
        self,
        client: TestClient,
        auth_headers: dict,
        test_client_model: Client
    ):
        """Test creating client with duplicate email"""
        response = client.post(
            "/api/v1/clients",
            headers=auth_headers,
            json={
                "name": "Duplicate Email",
                "email": test_client_model.email,
                "password": "password"
            }
        )

        assert response.status_code == 400

    def test_create_client_unauthorized(self, client: TestClient):
        """Test creating client without authentication"""
        response = client.post(
            "/api/v1/clients",
            json={
                "name": "Test Client",
                "email": "test@example.com"
            }
        )

        assert response.status_code == 401


@pytest.mark.unit
class TestGetClient:
    """Tests for GET /api/v1/clients/{id}"""

    def test_get_client_success(
        self,
        client: TestClient,
        auth_headers: dict,
        test_client_model: Client
    ):
        """Test getting client details"""
        response = client.get(
            f"/api/v1/clients/{test_client_model.id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["id"] == str(test_client_model.id)
        assert data["data"]["name"] == test_client_model.name
        assert data["data"]["email"] == test_client_model.email

    def test_get_client_not_found(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test getting non-existent client"""
        response = client.get(
            f"/api/v1/clients/{uuid4()}",
            headers=auth_headers
        )

        assert response.status_code == 404

    def test_get_client_unauthorized(
        self,
        client: TestClient,
        test_client_model: Client
    ):
        """Test getting client without authentication"""
        response = client.get(f"/api/v1/clients/{test_client_model.id}")

        assert response.status_code == 401


@pytest.mark.unit
class TestUpdateClient:
    """Tests for PATCH /api/v1/clients/{id}"""

    def test_update_client_success(
        self,
        client: TestClient,
        auth_headers: dict,
        test_client_model: Client
    ):
        """Test updating client"""
        response = client.patch(
            f"/api/v1/clients/{test_client_model.id}",
            headers=auth_headers,
            json={
                "name": "Updated Name",
                "phone": "+1111111111"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["name"] == "Updated Name"
        assert data["data"]["phone"] == "+1111111111"

    def test_update_client_email(
        self,
        client: TestClient,
        auth_headers: dict,
        test_client_model: Client
    ):
        """Test updating client email"""
        response = client.patch(
            f"/api/v1/clients/{test_client_model.id}",
            headers=auth_headers,
            json={"email": "newemail@example.com"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["email"] == "newemail@example.com"

    def test_update_client_avatar(
        self,
        client: TestClient,
        auth_headers: dict,
        test_client_model: Client
    ):
        """Test updating client avatar"""
        response = client.patch(
            f"/api/v1/clients/{test_client_model.id}",
            headers=auth_headers,
            json={"avatar": "https://example.com/new-avatar.jpg"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["avatar"] == "https://example.com/new-avatar.jpg"

    def test_update_client_not_found(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test updating non-existent client"""
        response = client.patch(
            f"/api/v1/clients/{uuid4()}",
            headers=auth_headers,
            json={"name": "Updated"}
        )

        assert response.status_code == 404

    def test_update_client_invalid_email(
        self,
        client: TestClient,
        auth_headers: dict,
        test_client_model: Client
    ):
        """Test updating with invalid email format"""
        response = client.patch(
            f"/api/v1/clients/{test_client_model.id}",
            headers=auth_headers,
            json={"email": "not-an-email"}
        )

        assert response.status_code == 422

    def test_update_client_unauthorized(
        self,
        client: TestClient,
        test_client_model: Client
    ):
        """Test updating client without authentication"""
        response = client.patch(
            f"/api/v1/clients/{test_client_model.id}",
            json={"name": "Updated"}
        )

        assert response.status_code == 401


@pytest.mark.unit
class TestDeleteClient:
    """Tests for DELETE /api/v1/clients/{id}"""

    def test_delete_client_success(
        self,
        client: TestClient,
        auth_headers: dict,
        db: Session
    ):
        """Test deleting client"""
        # Create a client without galleries
        test_client = Client(
            name="To Delete",
            email="delete@example.com",
            hashed_password="hashed_password"
        )
        db.add(test_client)
        db.commit()

        response = client.delete(
            f"/api/v1/clients/{test_client.id}",
            headers=auth_headers
        )

        assert response.status_code == 204

    def test_delete_client_not_found(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test deleting non-existent client"""
        response = client.delete(
            f"/api/v1/clients/{uuid4()}",
            headers=auth_headers
        )

        assert response.status_code == 404

    def test_delete_client_unauthorized(
        self,
        client: TestClient,
        test_client_model: Client
    ):
        """Test deleting client without authentication"""
        response = client.delete(f"/api/v1/clients/{test_client_model.id}")

        assert response.status_code == 401


@pytest.mark.unit
class TestGetClientGalleries:
    """Tests for GET /api/v1/clients/{id}/galleries"""

    def test_get_client_galleries_success(
        self,
        client: TestClient,
        auth_headers: dict,
        test_client_model: Client,
        test_gallery
    ):
        """Test getting all galleries for a client"""
        response = client.get(
            f"/api/v1/clients/{test_client_model.id}/galleries",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)
        assert len(data["data"]) >= 1

    def test_get_client_galleries_empty(
        self,
        client: TestClient,
        auth_headers: dict,
        db: Session
    ):
        """Test getting galleries for client with no galleries"""
        test_client = Client(
            name="No Galleries",
            email="nogalleries@example.com",
            hashed_password="hashed_password"
        )
        db.add(test_client)
        db.commit()

        response = client.get(
            f"/api/v1/clients/{test_client.id}/galleries",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 0

    def test_get_client_galleries_not_found(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test getting galleries for non-existent client"""
        response = client.get(
            f"/api/v1/clients/{uuid4()}/galleries",
            headers=auth_headers
        )

        assert response.status_code == 404

    def test_get_client_galleries_unauthorized(
        self,
        client: TestClient,
        test_client_model: Client
    ):
        """Test getting client galleries without authentication"""
        response = client.get(
            f"/api/v1/clients/{test_client_model.id}/galleries"
        )

        assert response.status_code == 401


@pytest.mark.unit
class TestClientModel:
    """Tests for Client model properties"""

    def test_client_has_galleries_count(
        self,
        client: TestClient,
        auth_headers: dict,
        test_client_model: Client,
        test_gallery
    ):
        """Test that client response includes galleries count"""
        response = client.get(
            f"/api/v1/clients/{test_client_model.id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "galleries_count" in data["data"]
        assert data["data"]["galleries_count"] >= 1

    def test_client_has_last_activity(
        self,
        client: TestClient,
        auth_headers: dict,
        test_client_model: Client
    ):
        """Test that client response includes last_activity"""
        response = client.get(
            f"/api/v1/clients/{test_client_model.id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "last_activity" in data["data"]

    def test_client_timestamps(
        self,
        client: TestClient,
        auth_headers: dict,
        test_client_model: Client
    ):
        """Test that client has created_at and updated_at timestamps"""
        response = client.get(
            f"/api/v1/clients/{test_client_model.id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "created_at" in data["data"]
        assert "updated_at" in data["data"]
