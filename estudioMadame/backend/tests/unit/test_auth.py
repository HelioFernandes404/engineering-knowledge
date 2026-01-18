"""
Unit tests for Authentication endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.user import User


@pytest.mark.unit
class TestAuthLogin:
    """Tests for POST /api/v1/auth/login"""

    def test_login_success(self, client: TestClient, test_user: User):
        """Test successful login with valid credentials"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@test.com",
                "password": "test123"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "access_token" in data["data"]
        assert "refresh_token" in data["data"]
        assert "expires_in" in data["data"]
        assert data["data"]["user"]["email"] == "admin@test.com"
        assert data["data"]["user"]["role"] == "admin"

    def test_login_invalid_email(self, client: TestClient):
        """Test login with non-existent email"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@test.com",
                "password": "password123"
            }
        )

        assert response.status_code == 401
        data = response.json()
        assert "error" in data

    def test_login_invalid_password(self, client: TestClient, test_user: User):
        """Test login with incorrect password"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@test.com",
                "password": "wrongpassword"
            }
        )

        assert response.status_code == 401
        data = response.json()
        assert "error" in data

    def test_login_missing_fields(self, client: TestClient):
        """Test login with missing required fields"""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "admin@test.com"}
        )

        assert response.status_code == 422

    def test_login_invalid_email_format(self, client: TestClient):
        """Test login with invalid email format"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "not-an-email",
                "password": "password123"
            }
        )

        assert response.status_code == 422


@pytest.mark.unit
class TestAuthRefresh:
    """Tests for POST /api/v1/auth/refresh"""

    def test_refresh_token_success(self, client: TestClient, test_user: User):
        """Test successful token refresh"""
        # First login to get refresh token
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@test.com",
                "password": "test123"
            }
        )
        refresh_token = login_response.json()["data"]["refresh_token"]

        # Now refresh
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token}
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data["data"]
        assert "expires_in" in data["data"]

    def test_refresh_token_invalid(self, client: TestClient):
        """Test refresh with invalid token"""
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid_token"}
        )

        assert response.status_code == 401

    def test_refresh_token_missing(self, client: TestClient):
        """Test refresh without token"""
        response = client.post(
            "/api/v1/auth/refresh",
            json={}
        )

        assert response.status_code == 422


@pytest.mark.unit
class TestAuthLogout:
    """Tests for POST /api/v1/auth/logout"""

    def test_logout_success(self, client: TestClient, auth_headers: dict):
        """Test successful logout"""
        response = client.post(
            "/api/v1/auth/logout",
            headers=auth_headers
        )

        assert response.status_code == 204

    def test_logout_no_token(self, client: TestClient):
        """Test logout without authorization header"""
        response = client.post("/api/v1/auth/logout")

        assert response.status_code == 401

    def test_logout_invalid_token(self, client: TestClient):
        """Test logout with invalid token"""
        response = client.post(
            "/api/v1/auth/logout",
            headers={"Authorization": "Bearer invalid_token"}
        )

        assert response.status_code == 401


@pytest.mark.unit
class TestGalleryAccessToken:
    """Tests for POST /api/v1/auth/gallery-access"""

    def test_generate_gallery_access_token_success(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery
    ):
        """Test successful generation of gallery access token"""
        response = client.post(
            "/api/v1/auth/gallery-access",
            headers=auth_headers,
            json={"gallery_id": str(test_gallery.id)}
        )

        assert response.status_code == 200
        data = response.json()
        assert "gallery_access_token" in data["data"]
        assert data["data"]["gallery_id"] == str(test_gallery.id)
        assert "expires_at" in data["data"]

    def test_generate_gallery_access_token_with_password(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery
    ):
        """Test generating token for password-protected gallery"""
        # Update gallery to have password protection
        test_gallery.settings = {"privacy": "password", "password": "secret123"}

        response = client.post(
            "/api/v1/auth/gallery-access",
            headers=auth_headers,
            json={
                "gallery_id": str(test_gallery.id),
                "password": "secret123"
            }
        )

        assert response.status_code == 200

    def test_generate_gallery_access_token_wrong_password(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery
    ):
        """Test generating token with wrong password"""
        test_gallery.settings = {"privacy": "password", "password": "secret123"}

        response = client.post(
            "/api/v1/auth/gallery-access",
            headers=auth_headers,
            json={
                "gallery_id": str(test_gallery.id),
                "password": "wrongpassword"
            }
        )

        assert response.status_code == 403

    def test_generate_gallery_access_token_not_found(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test generating token for non-existent gallery"""
        response = client.post(
            "/api/v1/auth/gallery-access",
            headers=auth_headers,
            json={"gallery_id": "00000000-0000-0000-0000-000000000000"}
        )

        assert response.status_code == 404

    def test_generate_gallery_access_token_unauthorized(
        self,
        client: TestClient,
        test_gallery
    ):
        """Test generating token without authentication"""
        response = client.post(
            "/api/v1/auth/gallery-access",
            json={"gallery_id": str(test_gallery.id)}
        )

        assert response.status_code == 401


@pytest.mark.unit
class TestVerifyGalleryAccess:
    """Tests for POST /api/v1/auth/verify-gallery-access"""

    def test_verify_gallery_access_valid_token(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery
    ):
        """Test verifying a valid gallery access token"""
        # First generate a token
        generate_response = client.post(
            "/api/v1/auth/gallery-access",
            headers=auth_headers,
            json={"gallery_id": str(test_gallery.id)}
        )
        token = generate_response.json()["data"]["gallery_access_token"]

        # Now verify it
        response = client.post(
            "/api/v1/auth/verify-gallery-access",
            json={
                "gallery_access_token": token,
                "gallery_id": str(test_gallery.id)
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["valid"] is True
        assert "gallery" in data["data"]

    def test_verify_gallery_access_invalid_token(
        self,
        client: TestClient,
        test_gallery
    ):
        """Test verifying an invalid token"""
        response = client.post(
            "/api/v1/auth/verify-gallery-access",
            json={
                "gallery_access_token": "invalid_token",
                "gallery_id": str(test_gallery.id)
            }
        )

        assert response.status_code == 403

    def test_verify_gallery_access_expired_token(
        self,
        client: TestClient,
        test_gallery
    ):
        """Test verifying an expired token"""
        # This would require mocking time or creating an expired token
        # For now, we'll just test with invalid token
        response = client.post(
            "/api/v1/auth/verify-gallery-access",
            json={
                "gallery_access_token": "expired_token",
                "gallery_id": str(test_gallery.id)
            }
        )

        assert response.status_code == 403
