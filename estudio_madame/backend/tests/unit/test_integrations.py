"""
Unit tests for Google Drive Integration endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import Mock, patch

from app.models.user import User
from app.models.google_drive_integration import GoogleDriveIntegration


@pytest.fixture
def test_drive_integration(db: Session, test_user: User) -> GoogleDriveIntegration:
    """Create a test Google Drive integration"""
    integration = GoogleDriveIntegration(
        user_id=test_user.id,
        access_token="enc_access_token",
        refresh_token="enc_refresh_token",
        email="testuser@gmail.com",
        status="active"
    )
    db.add(integration)
    db.commit()
    db.refresh(integration)
    return integration


@pytest.mark.unit
class TestGoogleDriveAuthURL:
    """Tests for GET /api/v1/integrations/google-drive/auth-url"""

    def test_get_auth_url_success(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test getting Google Drive OAuth URL"""
        response = client.get(
            "/api/v1/integrations/google-drive/auth-url",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "auth_url" in data["data"]
        assert "https://accounts.google.com" in data["data"]["auth_url"]
        assert "oauth2" in data["data"]["auth_url"]

    def test_get_auth_url_unauthorized(self, client: TestClient):
        """Test getting auth URL without authentication"""
        response = client.get(
            "/api/v1/integrations/google-drive/auth-url"
        )

        assert response.status_code == 401


@pytest.mark.unit
class TestGoogleDriveCallback:
    """Tests for POST /api/v1/integrations/google-drive/callback"""

    @patch('app.services.google_drive.GoogleDriveService.exchange_code_for_tokens')
    def test_callback_success(
        self,
        mock_exchange: Mock,
        client: TestClient,
        auth_headers: dict,
        test_user: User
    ):
        """Test successful OAuth callback"""
        # Mock the token exchange
        mock_exchange.return_value = {
            "access_token": "new_access_token",
            "refresh_token": "new_refresh_token",
            "email": "testuser@gmail.com"
        }

        response = client.post(
            "/api/v1/integrations/google-drive/callback",
            headers=auth_headers,
            json={"code": "oauth_authorization_code"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert data["data"]["email"] == "testuser@gmail.com"
        assert data["data"]["status"] == "active"
        assert "id" in data["data"]

    def test_callback_missing_code(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test callback without authorization code"""
        response = client.post(
            "/api/v1/integrations/google-drive/callback",
            headers=auth_headers,
            json={}
        )

        assert response.status_code == 422

    @patch('app.services.google_drive.GoogleDriveService.exchange_code_for_tokens')
    def test_callback_invalid_code(
        self,
        mock_exchange: Mock,
        client: TestClient,
        auth_headers: dict
    ):
        """Test callback with invalid authorization code"""
        # Mock failed token exchange
        mock_exchange.side_effect = Exception("Invalid authorization code")

        response = client.post(
            "/api/v1/integrations/google-drive/callback",
            headers=auth_headers,
            json={"code": "invalid_code"}
        )

        assert response.status_code == 400

    def test_callback_unauthorized(self, client: TestClient):
        """Test callback without authentication"""
        response = client.post(
            "/api/v1/integrations/google-drive/callback",
            json={"code": "some_code"}
        )

        assert response.status_code == 401


@pytest.mark.unit
class TestGoogleDriveStatus:
    """Tests for GET /api/v1/integrations/google-drive/status"""

    def test_get_status_success(
        self,
        client: TestClient,
        auth_headers: dict,
        test_drive_integration: GoogleDriveIntegration
    ):
        """Test getting integration status when connected"""
        response = client.get(
            "/api/v1/integrations/google-drive/status",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert data["data"]["email"] == "testuser@gmail.com"
        assert data["data"]["status"] == "active"
        assert "connected_at" in data["data"]

    def test_get_status_not_connected(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test getting status when not connected"""
        response = client.get(
            "/api/v1/integrations/google-drive/status",
            headers=auth_headers
        )

        # Should return 404 or null data when not connected
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.json()
            assert data["data"] is None or data["data"]["status"] == "disconnected"

    def test_get_status_expired_integration(
        self,
        client: TestClient,
        auth_headers: dict,
        test_drive_integration: GoogleDriveIntegration,
        db: Session
    ):
        """Test status when integration is expired"""
        test_drive_integration.status = "expired"
        db.commit()

        response = client.get(
            "/api/v1/integrations/google-drive/status",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["status"] == "expired"

    def test_get_status_unauthorized(self, client: TestClient):
        """Test getting status without authentication"""
        response = client.get(
            "/api/v1/integrations/google-drive/status"
        )

        assert response.status_code == 401


@pytest.mark.unit
class TestGoogleDriveDisconnect:
    """Tests for DELETE /api/v1/integrations/google-drive/disconnect"""

    @patch('app.services.google_drive.GoogleDriveService.revoke_tokens')
    def test_disconnect_success(
        self,
        mock_revoke: Mock,
        client: TestClient,
        auth_headers: dict,
        test_drive_integration: GoogleDriveIntegration
    ):
        """Test disconnecting Google Drive integration"""
        response = client.delete(
            "/api/v1/integrations/google-drive/disconnect",
            headers=auth_headers
        )

        assert response.status_code == 204
        mock_revoke.assert_called_once()

    def test_disconnect_not_connected(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test disconnecting when not connected"""
        response = client.delete(
            "/api/v1/integrations/google-drive/disconnect",
            headers=auth_headers
        )

        # Should handle gracefully
        assert response.status_code in [204, 404]

    def test_disconnect_unauthorized(self, client: TestClient):
        """Test disconnecting without authentication"""
        response = client.delete(
            "/api/v1/integrations/google-drive/disconnect"
        )

        assert response.status_code == 401


@pytest.mark.unit
class TestGoogleDriveFolders:
    """Tests for GET /api/v1/integrations/google-drive/folders"""

    @patch('app.services.google_drive.GoogleDriveService.list_folders')
    def test_list_folders_success(
        self,
        mock_list_folders: Mock,
        client: TestClient,
        auth_headers: dict,
        test_drive_integration: GoogleDriveIntegration
    ):
        """Test listing Google Drive folders"""
        # Mock folder list
        mock_list_folders.return_value = [
            {
                "id": "folder_1",
                "name": "Wedding Photos",
                "web_view_link": "https://drive.google.com/folder_1",
                "created_time": "2024-01-01T00:00:00Z"
            },
            {
                "id": "folder_2",
                "name": "Portrait Sessions",
                "web_view_link": "https://drive.google.com/folder_2",
                "created_time": "2024-01-15T00:00:00Z"
            }
        ]

        response = client.get(
            "/api/v1/integrations/google-drive/folders",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["data"]) == 2
        assert data["data"][0]["name"] == "Wedding Photos"
        assert data["data"][1]["name"] == "Portrait Sessions"

    @patch('app.services.google_drive.GoogleDriveService.list_folders')
    def test_list_folders_with_parent(
        self,
        mock_list_folders: Mock,
        client: TestClient,
        auth_headers: dict,
        test_drive_integration: GoogleDriveIntegration
    ):
        """Test listing folders within a specific parent folder"""
        mock_list_folders.return_value = [
            {
                "id": "subfolder_1",
                "name": "2024 Weddings",
                "web_view_link": "https://drive.google.com/subfolder_1",
                "created_time": "2024-01-01T00:00:00Z"
            }
        ]

        response = client.get(
            "/api/v1/integrations/google-drive/folders?parent_id=folder_1",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 1
        mock_list_folders.assert_called_with(parent_id="folder_1", search=None)

    @patch('app.services.google_drive.GoogleDriveService.list_folders')
    def test_list_folders_with_search(
        self,
        mock_list_folders: Mock,
        client: TestClient,
        auth_headers: dict,
        test_drive_integration: GoogleDriveIntegration
    ):
        """Test searching folders by name"""
        mock_list_folders.return_value = [
            {
                "id": "folder_1",
                "name": "Wedding Photos 2024",
                "web_view_link": "https://drive.google.com/folder_1",
                "created_time": "2024-01-01T00:00:00Z"
            }
        ]

        response = client.get(
            "/api/v1/integrations/google-drive/folders?search=Wedding",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) >= 1
        mock_list_folders.assert_called_with(parent_id=None, search="Wedding")

    def test_list_folders_not_connected(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test listing folders when not connected to Drive"""
        response = client.get(
            "/api/v1/integrations/google-drive/folders",
            headers=auth_headers
        )

        # Should return error when not connected
        assert response.status_code in [400, 403, 404]

    @patch('app.services.google_drive.GoogleDriveService.list_folders')
    def test_list_folders_expired_token(
        self,
        mock_list_folders: Mock,
        client: TestClient,
        auth_headers: dict,
        test_drive_integration: GoogleDriveIntegration,
        db: Session
    ):
        """Test listing folders with expired token"""
        test_drive_integration.status = "expired"
        db.commit()

        mock_list_folders.side_effect = Exception("Token expired")

        response = client.get(
            "/api/v1/integrations/google-drive/folders",
            headers=auth_headers
        )

        # Should handle expired token gracefully
        assert response.status_code in [400, 401, 403]

    def test_list_folders_unauthorized(self, client: TestClient):
        """Test listing folders without authentication"""
        response = client.get(
            "/api/v1/integrations/google-drive/folders"
        )

        assert response.status_code == 401


@pytest.mark.unit
class TestGoogleDriveIntegrationModel:
    """Tests for Google Drive integration model fields"""

    def test_integration_has_required_fields(
        self,
        client: TestClient,
        auth_headers: dict,
        test_drive_integration: GoogleDriveIntegration
    ):
        """Test that integration has all required fields"""
        response = client.get(
            "/api/v1/integrations/google-drive/status",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        integration = data["data"]

        assert "id" in integration
        assert "user_id" in integration
        assert "email" in integration
        assert "status" in integration
        assert "connected_at" in integration

    def test_integration_hides_sensitive_fields(
        self,
        client: TestClient,
        auth_headers: dict,
        test_drive_integration: GoogleDriveIntegration
    ):
        """Test that sensitive fields are not exposed"""
        response = client.get(
            "/api/v1/integrations/google-drive/status",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        integration = data["data"]

        # Tokens should not be exposed in API response
        assert "access_token" not in integration
        assert "refresh_token" not in integration

    def test_integration_status_values(
        self,
        client: TestClient,
        auth_headers: dict,
        test_drive_integration: GoogleDriveIntegration,
        db: Session
    ):
        """Test valid integration status values"""
        valid_statuses = ["active", "expired", "disconnected"]

        for status in valid_statuses:
            test_drive_integration.status = status
            db.commit()

            response = client.get(
                "/api/v1/integrations/google-drive/status",
                headers=auth_headers
            )

            assert response.status_code == 200
            data = response.json()
            assert data["data"]["status"] == status
