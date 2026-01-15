"""
Unit tests for Dashboard endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.gallery import Gallery
from app.models.client import Client


@pytest.mark.unit
class TestDashboardStats:
    """Tests for GET /api/v1/dashboard/stats"""

    def test_get_dashboard_stats_success(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery: Gallery,
        test_client_model: Client
    ):
        """Test getting dashboard statistics"""
        response = client.get(
            "/api/v1/dashboard/stats",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "active_galleries" in data["data"]
        assert "total_clients" in data["data"]
        assert "storage_used_bytes" in data["data"]
        assert "storage_total_bytes" in data["data"]
        assert "storage_percentage" in data["data"]

    def test_dashboard_stats_count_active_galleries(
        self,
        client: TestClient,
        auth_headers: dict,
        db: Session,
        test_client_model: Client
    ):
        """Test that active galleries count is correct"""
        # Create multiple galleries with different statuses
        for i, status in enumerate(["published", "draft", "client_selection"]):
            gallery = Gallery(
                title=f"Gallery {i}",
                client_id=test_client_model.id,
                status=status
            )
            db.add(gallery)
        db.commit()

        response = client.get(
            "/api/v1/dashboard/stats",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        # Active galleries = published + client_selection (not archived/draft)
        assert data["data"]["active_galleries"] >= 2

    def test_dashboard_stats_count_total_clients(
        self,
        client: TestClient,
        auth_headers: dict,
        db: Session
    ):
        """Test that total clients count is correct"""
        # Create multiple clients
        for i in range(3):
            client_model = Client(
                name=f"Client {i}",
                email=f"client{i}@example.com",
                hashed_password="hashed_password"
            )
            db.add(client_model)
        db.commit()

        response = client.get(
            "/api/v1/dashboard/stats",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["total_clients"] >= 3

    def test_dashboard_stats_storage_calculation(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test storage calculation"""
        response = client.get(
            "/api/v1/dashboard/stats",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        storage = data["data"]

        # Verify storage percentage is calculated correctly
        assert 0 <= storage["storage_percentage"] <= 100

        # Verify relationship between used and total
        if storage["storage_total_bytes"] > 0:
            calculated_percentage = (
                storage["storage_used_bytes"] / storage["storage_total_bytes"]
            ) * 100
            assert abs(calculated_percentage - storage["storage_percentage"]) < 0.01

    def test_dashboard_stats_unauthorized(self, client: TestClient):
        """Test getting stats without authentication"""
        response = client.get("/api/v1/dashboard/stats")

        assert response.status_code == 401

    def test_dashboard_stats_photographer_access(
        self,
        client: TestClient,
        photographer_headers: dict
    ):
        """Test that photographers can access dashboard stats"""
        response = client.get(
            "/api/v1/dashboard/stats",
            headers=photographer_headers
        )

        assert response.status_code == 200


@pytest.mark.unit
class TestRecentGalleries:
    """Tests for GET /api/v1/dashboard/recent-galleries"""

    def test_get_recent_galleries_success(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery: Gallery
    ):
        """Test getting recent galleries"""
        response = client.get(
            "/api/v1/dashboard/recent-galleries",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)
        assert len(data["data"]) >= 1

    def test_recent_galleries_default_limit(
        self,
        client: TestClient,
        auth_headers: dict,
        db: Session,
        test_client_model: Client
    ):
        """Test recent galleries default limit"""
        # Create more than 10 galleries
        for i in range(15):
            gallery = Gallery(
                title=f"Gallery {i}",
                client_id=test_client_model.id,
                status="published"
            )
            db.add(gallery)
        db.commit()

        response = client.get(
            "/api/v1/dashboard/recent-galleries",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        # Default limit should be 10
        assert len(data["data"]) <= 10

    def test_recent_galleries_custom_limit(
        self,
        client: TestClient,
        auth_headers: dict,
        db: Session,
        test_client_model: Client
    ):
        """Test recent galleries with custom limit"""
        # Create multiple galleries
        for i in range(7):
            gallery = Gallery(
                title=f"Gallery {i}",
                client_id=test_client_model.id,
                status="published"
            )
            db.add(gallery)
        db.commit()

        response = client.get(
            "/api/v1/dashboard/recent-galleries?limit=5",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) <= 5

    def test_recent_galleries_filter_all(
        self,
        client: TestClient,
        auth_headers: dict,
        db: Session,
        test_client_model: Client
    ):
        """Test filtering recent galleries with 'all' status"""
        response = client.get(
            "/api/v1/dashboard/recent-galleries?status_filter=all",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["data"], list)

    def test_recent_galleries_filter_editing(
        self,
        client: TestClient,
        auth_headers: dict,
        db: Session,
        test_client_model: Client
    ):
        """Test filtering recent galleries by 'editing' status"""
        # Create galleries with different dashboard statuses
        for i, status in enumerate(["draft", "published", "client_selection"]):
            gallery = Gallery(
                title=f"Gallery {i}",
                client_id=test_client_model.id,
                status=status
            )
            db.add(gallery)
        db.commit()

        response = client.get(
            "/api/v1/dashboard/recent-galleries?status_filter=editing",
            headers=auth_headers
        )

        assert response.status_code == 200
        # Should filter galleries appropriately

    def test_recent_galleries_filter_delivered(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test filtering recent galleries by 'delivered' status"""
        response = client.get(
            "/api/v1/dashboard/recent-galleries?status_filter=delivered",
            headers=auth_headers
        )

        assert response.status_code == 200

    def test_recent_galleries_ordered_by_date(
        self,
        client: TestClient,
        auth_headers: dict,
        db: Session,
        test_client_model: Client
    ):
        """Test that recent galleries are ordered by date"""
        # Create galleries
        from datetime import datetime, timedelta

        for i in range(3):
            gallery = Gallery(
                title=f"Gallery {i}",
                client_id=test_client_model.id,
                status="published",
                date_created=datetime.utcnow() - timedelta(days=i)
            )
            db.add(gallery)
        db.commit()

        response = client.get(
            "/api/v1/dashboard/recent-galleries",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()

        # Verify they're ordered by date (newest first)
        if len(data["data"]) > 1:
            dates = [g["date"] for g in data["data"]]
            # Dates should be in descending order
            assert dates == sorted(dates, reverse=True)

    def test_recent_galleries_unauthorized(self, client: TestClient):
        """Test getting recent galleries without authentication"""
        response = client.get("/api/v1/dashboard/recent-galleries")

        assert response.status_code == 401


@pytest.mark.unit
class TestDashboardGalleryFormat:
    """Tests for dashboard gallery data format"""

    def test_dashboard_gallery_has_required_fields(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery: Gallery
    ):
        """Test that dashboard gallery has all required fields"""
        response = client.get(
            "/api/v1/dashboard/recent-galleries",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()

        if len(data["data"]) > 0:
            gallery = data["data"][0]
            assert "id" in gallery
            assert "title" in gallery
            assert "date" in gallery
            assert "image" in gallery
            assert "status" in gallery
            assert "photos" in gallery
            assert "size" in gallery

    def test_dashboard_gallery_status_mapping(
        self,
        client: TestClient,
        auth_headers: dict,
        db: Session,
        test_client_model: Client
    ):
        """Test that gallery status is mapped correctly for dashboard"""
        gallery = Gallery(
            title="Test Gallery",
            client_id=test_client_model.id,
            status="published"
        )
        db.add(gallery)
        db.commit()

        response = client.get(
            "/api/v1/dashboard/recent-galleries",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()

        # Dashboard status should be one of: Delivered, Editing, Uploading, Selection
        if len(data["data"]) > 0:
            dashboard_status = data["data"][0]["status"]
            assert dashboard_status in ["Delivered", "Editing", "Uploading", "Selection"]

    def test_dashboard_gallery_size_format(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery: Gallery
    ):
        """Test that gallery size is formatted as human-readable string"""
        response = client.get(
            "/api/v1/dashboard/recent-galleries",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()

        if len(data["data"]) > 0:
            size = data["data"][0]["size"]
            # Size should be a string like "2.4 GB", "1.1 MB", etc.
            assert isinstance(size, str)
            assert any(unit in size for unit in ["B", "GB", "MB", "KB", "TB"])
