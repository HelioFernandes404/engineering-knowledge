"""
Unit tests for Galleries endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from uuid import uuid4

from app.models.gallery import Gallery
from app.models.client import Client


@pytest.mark.unit
class TestListGalleries:
    """Tests for GET /api/v1/galleries"""

    def test_list_galleries_success(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery: Gallery
    ):
        """Test listing galleries with authentication"""
        response = client.get(
            "/api/v1/galleries",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "meta" in data
        assert isinstance(data["data"], list)
        assert len(data["data"]) >= 1
        assert data["meta"]["page"] == 1

    def test_list_galleries_with_pagination(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test galleries pagination"""
        response = client.get(
            "/api/v1/galleries?page=1&limit=10",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["meta"]["page"] == 1
        assert data["meta"]["limit"] == 10

    def test_list_galleries_filter_by_status(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery: Gallery
    ):
        """Test filtering galleries by status"""
        response = client.get(
            "/api/v1/galleries?status=published",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        for gallery in data["data"]:
            assert gallery["status"] == "published"

    def test_list_galleries_search(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery: Gallery
    ):
        """Test searching galleries by title"""
        response = client.get(
            f"/api/v1/galleries?search=Test",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) >= 1

    def test_list_galleries_sort(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test sorting galleries"""
        response = client.get(
            "/api/v1/galleries?sort_by=title&order=asc",
            headers=auth_headers
        )

        assert response.status_code == 200

    def test_list_galleries_unauthorized(self, client: TestClient):
        """Test listing galleries without authentication"""
        response = client.get("/api/v1/galleries")

        assert response.status_code == 401


@pytest.mark.unit
class TestCreateGallery:
    """Tests for POST /api/v1/galleries"""

    def test_create_gallery_success(
        self,
        client: TestClient,
        auth_headers: dict,
        test_client_model: Client
    ):
        """Test creating a new gallery"""
        response = client.post(
            "/api/v1/galleries",
            headers=auth_headers,
            json={
                "title": "New Wedding Gallery",
                "description": "Beautiful wedding",
                "client_id": str(test_client_model.id),
                "event_date": "2024-12-25",
                "location": "Central Park, NY",
                "auto_sync_enabled": True,
                "settings": {
                    "privacy": "private",
                    "allow_downloads": True,
                    "mature_content": False,
                    "max_client_selection": 50,
                    "layout": "grid",
                    "default_sort": "newest"
                }
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["data"]["title"] == "New Wedding Gallery"
        assert data["data"]["client_id"] == str(test_client_model.id)
        assert "id" in data["data"]
        assert "access_token" in data["data"]

    def test_create_gallery_minimal_fields(
        self,
        client: TestClient,
        auth_headers: dict,
        test_client_model: Client
    ):
        """Test creating gallery with only required fields"""
        response = client.post(
            "/api/v1/galleries",
            headers=auth_headers,
            json={
                "title": "Minimal Gallery",
                "client_id": str(test_client_model.id)
            }
        )

        assert response.status_code == 201

    def test_create_gallery_with_google_drive(
        self,
        client: TestClient,
        auth_headers: dict,
        test_client_model: Client
    ):
        """Test creating gallery with Google Drive folder"""
        response = client.post(
            "/api/v1/galleries",
            headers=auth_headers,
            json={
                "title": "Drive Synced Gallery",
                "client_id": str(test_client_model.id),
                "google_drive_folder_id": "folder_123",
                "auto_sync_enabled": True
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["data"]["google_drive_folder_id"] == "folder_123"
        assert data["data"]["auto_sync_enabled"] is True

    def test_create_gallery_missing_required_fields(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test creating gallery without required fields"""
        response = client.post(
            "/api/v1/galleries",
            headers=auth_headers,
            json={"description": "Missing title and client_id"}
        )

        assert response.status_code == 422

    def test_create_gallery_invalid_client_id(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test creating gallery with non-existent client"""
        response = client.post(
            "/api/v1/galleries",
            headers=auth_headers,
            json={
                "title": "Test Gallery",
                "client_id": str(uuid4())
            }
        )

        assert response.status_code == 404

    def test_create_gallery_unauthorized(
        self,
        client: TestClient,
        test_client_model: Client
    ):
        """Test creating gallery without authentication"""
        response = client.post(
            "/api/v1/galleries",
            json={
                "title": "Test Gallery",
                "client_id": str(test_client_model.id)
            }
        )

        assert response.status_code == 401


@pytest.mark.unit
class TestGetGallery:
    """Tests for GET /api/v1/galleries/{id}"""

    def test_get_gallery_success(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery: Gallery
    ):
        """Test getting gallery details"""
        response = client.get(
            f"/api/v1/galleries/{test_gallery.id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["id"] == str(test_gallery.id)
        assert data["data"]["title"] == test_gallery.title
        assert "client" in data["data"]

    def test_get_gallery_not_found(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test getting non-existent gallery"""
        response = client.get(
            f"/api/v1/galleries/{uuid4()}",
            headers=auth_headers
        )

        assert response.status_code == 404

    def test_get_gallery_unauthorized(
        self,
        client: TestClient,
        test_gallery: Gallery
    ):
        """Test getting gallery without authentication"""
        response = client.get(f"/api/v1/galleries/{test_gallery.id}")

        assert response.status_code == 401


@pytest.mark.unit
class TestUpdateGallery:
    """Tests for PATCH /api/v1/galleries/{id}"""

    def test_update_gallery_success(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery: Gallery
    ):
        """Test updating gallery"""
        response = client.patch(
            f"/api/v1/galleries/{test_gallery.id}",
            headers=auth_headers,
            json={
                "title": "Updated Gallery Title",
                "status": "archived"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["title"] == "Updated Gallery Title"
        assert data["data"]["status"] == "archived"

    def test_update_gallery_settings(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery: Gallery
    ):
        """Test updating gallery settings"""
        response = client.patch(
            f"/api/v1/galleries/{test_gallery.id}",
            headers=auth_headers,
            json={
                "settings": {
                    "allow_downloads": False,
                    "privacy": "password",
                    "password": "new_password"
                }
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["settings"]["allow_downloads"] is False

    def test_update_gallery_not_found(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test updating non-existent gallery"""
        response = client.patch(
            f"/api/v1/galleries/{uuid4()}",
            headers=auth_headers,
            json={"title": "Updated"}
        )

        assert response.status_code == 404

    def test_update_gallery_unauthorized(
        self,
        client: TestClient,
        test_gallery: Gallery
    ):
        """Test updating gallery without authentication"""
        response = client.patch(
            f"/api/v1/galleries/{test_gallery.id}",
            json={"title": "Updated"}
        )

        assert response.status_code == 401


@pytest.mark.unit
class TestDeleteGallery:
    """Tests for DELETE /api/v1/galleries/{id}"""

    def test_delete_gallery_success(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery: Gallery
    ):
        """Test deleting gallery"""
        response = client.delete(
            f"/api/v1/galleries/{test_gallery.id}",
            headers=auth_headers
        )

        assert response.status_code == 204

    def test_delete_gallery_not_found(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test deleting non-existent gallery"""
        response = client.delete(
            f"/api/v1/galleries/{uuid4()}",
            headers=auth_headers
        )

        assert response.status_code == 404

    def test_delete_gallery_unauthorized(
        self,
        client: TestClient,
        test_gallery: Gallery
    ):
        """Test deleting gallery without authentication"""
        response = client.delete(f"/api/v1/galleries/{test_gallery.id}")

        assert response.status_code == 401


@pytest.mark.unit
class TestBulkGalleryActions:
    """Tests for POST /api/v1/galleries/bulk-action"""

    def test_bulk_delete_galleries(
        self,
        client: TestClient,
        auth_headers: dict,
        db: Session,
        test_client_model: Client
    ):
        """Test bulk deleting galleries"""
        # Create multiple galleries
        galleries = []
        for i in range(3):
            gallery = Gallery(
                title=f"Gallery {i}",
                client_id=test_client_model.id,
                status="draft"
            )
            db.add(gallery)
            galleries.append(gallery)
        db.commit()

        gallery_ids = [str(g.id) for g in galleries]

        response = client.post(
            "/api/v1/galleries/bulk-action",
            headers=auth_headers,
            json={
                "action": "delete",
                "gallery_ids": gallery_ids
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["success_count"] == 3
        assert data["data"]["failed_count"] == 0

    def test_bulk_change_status(
        self,
        client: TestClient,
        auth_headers: dict,
        db: Session,
        test_client_model: Client
    ):
        """Test bulk changing gallery status"""
        galleries = []
        for i in range(2):
            gallery = Gallery(
                title=f"Gallery {i}",
                client_id=test_client_model.id,
                status="draft"
            )
            db.add(gallery)
            galleries.append(gallery)
        db.commit()

        gallery_ids = [str(g.id) for g in galleries]

        response = client.post(
            "/api/v1/galleries/bulk-action",
            headers=auth_headers,
            json={
                "action": "change_status",
                "gallery_ids": gallery_ids,
                "params": {"status": "published"}
            }
        )

        assert response.status_code == 200

    def test_bulk_action_unauthorized(self, client: TestClient):
        """Test bulk action without authentication"""
        response = client.post(
            "/api/v1/galleries/bulk-action",
            json={
                "action": "delete",
                "gallery_ids": [str(uuid4())]
            }
        )

        assert response.status_code == 401


@pytest.mark.unit
class TestGallerySync:
    """Tests for gallery sync endpoints"""

    def test_sync_gallery_with_drive(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery: Gallery
    ):
        """Test syncing gallery with Google Drive"""
        # Set up gallery with Drive folder
        test_gallery.google_drive_folder_id = "folder_123"
        test_gallery.auto_sync_enabled = True

        response = client.post(
            f"/api/v1/galleries/{test_gallery.id}/sync",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "sync_job_id" in data["data"]
        assert data["data"]["status"] == "running"

    def test_get_sync_status(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery: Gallery
    ):
        """Test getting sync status"""
        response = client.get(
            f"/api/v1/galleries/{test_gallery.id}/sync-status",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "status" in data["data"]


@pytest.mark.unit
class TestPublicGalleryAccess:
    """Tests for GET /api/v1/galleries/{id}/public"""

    def test_get_public_gallery_with_valid_token(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery: Gallery
    ):
        """Test accessing public gallery with valid token"""
        # Generate access token first
        token_response = client.post(
            "/api/v1/auth/gallery-access",
            headers=auth_headers,
            json={"gallery_id": str(test_gallery.id)}
        )
        access_token = token_response.json()["data"]["gallery_access_token"]

        # Access public gallery
        response = client.get(
            f"/api/v1/galleries/{test_gallery.id}/public?access_token={access_token}"
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["id"] == str(test_gallery.id)
        assert "title" in data["data"]
        assert "settings" in data["data"]

    def test_get_public_gallery_invalid_token(
        self,
        client: TestClient,
        test_gallery: Gallery
    ):
        """Test accessing public gallery with invalid token"""
        response = client.get(
            f"/api/v1/galleries/{test_gallery.id}/public?access_token=invalid"
        )

        assert response.status_code == 403

    def test_get_public_gallery_no_token(
        self,
        client: TestClient,
        test_gallery: Gallery
    ):
        """Test accessing public gallery without token"""
        response = client.get(
            f"/api/v1/galleries/{test_gallery.id}/public"
        )

        assert response.status_code == 403
