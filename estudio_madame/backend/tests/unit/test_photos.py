"""
Unit tests for Photos endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from uuid import uuid4

from app.models.gallery import Gallery
from app.models.photo import Photo


@pytest.fixture
def test_photo(db: Session, test_gallery: Gallery) -> Photo:
    """Create a test photo"""
    photo = Photo(
        gallery_id=test_gallery.id,
        google_drive_file_id="drive_file_123",
        google_drive_web_view_link="https://drive.google.com/file/d/123",
        google_drive_thumbnail_link="https://drive.google.com/thumbnail/123",
        google_drive_download_link="https://drive.google.com/uc?id=123",
        file_name="wedding_photo_001.jpg",
        file_size=2_500_000,
        mime_type="image/jpeg",
        width=1920,
        height=1080,
        selected_by_client=False
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo


@pytest.mark.unit
class TestListGalleryPhotos:
    """Tests for GET /api/v1/galleries/{gallery_id}/photos"""

    def test_list_photos_success(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery: Gallery,
        test_photo: Photo
    ):
        """Test listing photos in a gallery"""
        response = client.get(
            f"/api/v1/galleries/{test_gallery.id}/photos",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "meta" in data
        assert isinstance(data["data"], list)
        assert len(data["data"]) >= 1

    def test_list_photos_with_pagination(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery: Gallery
    ):
        """Test photo pagination"""
        response = client.get(
            f"/api/v1/galleries/{test_gallery.id}/photos?page=1&limit=50",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["meta"]["page"] == 1
        assert data["meta"]["limit"] == 50

    def test_list_photos_filter_by_client_selection(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery: Gallery,
        db: Session
    ):
        """Test filtering photos by client selection"""
        # Create photos with different selection status
        selected_photo = Photo(
            gallery_id=test_gallery.id,
            google_drive_file_id="selected_123",
            file_name="selected.jpg",
            file_size=1000000,
            mime_type="image/jpeg",
            selected_by_client=True
        )
        db.add(selected_photo)
        db.commit()

        response = client.get(
            f"/api/v1/galleries/{test_gallery.id}/photos?selected_by_client=true",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        for photo in data["data"]:
            assert photo["selected_by_client"] is True

    def test_list_photos_gallery_not_found(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test listing photos for non-existent gallery"""
        response = client.get(
            f"/api/v1/galleries/{uuid4()}/photos",
            headers=auth_headers
        )

        assert response.status_code == 404

    def test_list_photos_unauthorized(
        self,
        client: TestClient,
        test_gallery: Gallery
    ):
        """Test listing photos without authentication"""
        response = client.get(
            f"/api/v1/galleries/{test_gallery.id}/photos"
        )

        assert response.status_code == 401


@pytest.mark.unit
class TestListPublicGalleryPhotos:
    """Tests for GET /api/v1/galleries/{gallery_id}/photos/public"""

    def test_list_public_photos_with_valid_token(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery: Gallery,
        test_photo: Photo
    ):
        """Test listing photos as a client with valid access token"""
        # Generate access token
        token_response = client.post(
            "/api/v1/auth/gallery-access",
            headers=auth_headers,
            json={"gallery_id": str(test_gallery.id)}
        )
        access_token = token_response.json()["data"]["gallery_access_token"]

        # List photos
        response = client.get(
            f"/api/v1/galleries/{test_gallery.id}/photos/public?access_token={access_token}"
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["data"], list)
        assert len(data["data"]) >= 1
        # Check that photo has all necessary fields for client
        photo = data["data"][0]
        assert "id" in photo
        assert "google_drive_thumbnail_link" in photo
        assert "file_name" in photo

    def test_list_public_photos_invalid_token(
        self,
        client: TestClient,
        test_gallery: Gallery
    ):
        """Test listing public photos with invalid token"""
        response = client.get(
            f"/api/v1/galleries/{test_gallery.id}/photos/public?access_token=invalid"
        )

        assert response.status_code == 403

    def test_list_public_photos_no_token(
        self,
        client: TestClient,
        test_gallery: Gallery
    ):
        """Test listing public photos without token"""
        response = client.get(
            f"/api/v1/galleries/{test_gallery.id}/photos/public"
        )

        assert response.status_code == 403

    def test_list_public_photos_with_pagination(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery: Gallery
    ):
        """Test public photos pagination"""
        # Generate token
        token_response = client.post(
            "/api/v1/auth/gallery-access",
            headers=auth_headers,
            json={"gallery_id": str(test_gallery.id)}
        )
        access_token = token_response.json()["data"]["gallery_access_token"]

        response = client.get(
            f"/api/v1/galleries/{test_gallery.id}/photos/public"
            f"?access_token={access_token}&page=1&limit=20"
        )

        assert response.status_code == 200
        data = response.json()
        assert data["meta"]["limit"] == 20


@pytest.mark.unit
class TestSelectPhoto:
    """Tests for POST /api/v1/photos/{id}/select"""

    def test_select_photo_success(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery: Gallery,
        test_photo: Photo
    ):
        """Test client selecting a photo"""
        # Generate access token
        token_response = client.post(
            "/api/v1/auth/gallery-access",
            headers=auth_headers,
            json={"gallery_id": str(test_gallery.id)}
        )
        access_token = token_response.json()["data"]["gallery_access_token"]

        # Select photo
        response = client.post(
            f"/api/v1/photos/{test_photo.id}/select",
            json={
                "gallery_access_token": access_token,
                "selected": True
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["photo_id"] == str(test_photo.id)
        assert data["data"]["selected"] is True
        assert "current_selection_count" in data["data"]

    def test_deselect_photo_success(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery: Gallery,
        test_photo: Photo
    ):
        """Test client deselecting a photo"""
        # Generate access token
        token_response = client.post(
            "/api/v1/auth/gallery-access",
            headers=auth_headers,
            json={"gallery_id": str(test_gallery.id)}
        )
        access_token = token_response.json()["data"]["gallery_access_token"]

        # First select
        client.post(
            f"/api/v1/photos/{test_photo.id}/select",
            json={
                "gallery_access_token": access_token,
                "selected": True
            }
        )

        # Then deselect
        response = client.post(
            f"/api/v1/photos/{test_photo.id}/select",
            json={
                "gallery_access_token": access_token,
                "selected": False
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["selected"] is False

    def test_select_photo_exceeds_limit(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery: Gallery,
        db: Session
    ):
        """Test selecting photo when limit is reached"""
        # Set gallery selection limit
        test_gallery.settings = {"max_client_selection": 2}
        db.commit()

        # Generate access token
        token_response = client.post(
            "/api/v1/auth/gallery-access",
            headers=auth_headers,
            json={"gallery_id": str(test_gallery.id)}
        )
        access_token = token_response.json()["data"]["gallery_access_token"]

        # Create and select 2 photos
        for i in range(2):
            photo = Photo(
                gallery_id=test_gallery.id,
                google_drive_file_id=f"photo_{i}",
                file_name=f"photo_{i}.jpg",
                file_size=1000000,
                mime_type="image/jpeg",
                selected_by_client=False
            )
            db.add(photo)
        db.commit()

        photos = db.query(Photo).filter(Photo.gallery_id == test_gallery.id).all()

        # Select first two
        for photo in photos[:2]:
            client.post(
                f"/api/v1/photos/{photo.id}/select",
                json={
                    "gallery_access_token": access_token,
                    "selected": True
                }
            )

        # Try to select third (should fail)
        third_photo = Photo(
            gallery_id=test_gallery.id,
            google_drive_file_id="photo_3",
            file_name="photo_3.jpg",
            file_size=1000000,
            mime_type="image/jpeg",
            selected_by_client=False
        )
        db.add(third_photo)
        db.commit()

        response = client.post(
            f"/api/v1/photos/{third_photo.id}/select",
            json={
                "gallery_access_token": access_token,
                "selected": True
            }
        )

        assert response.status_code == 403

    def test_select_photo_invalid_token(
        self,
        client: TestClient,
        test_photo: Photo
    ):
        """Test selecting photo with invalid token"""
        response = client.post(
            f"/api/v1/photos/{test_photo.id}/select",
            json={
                "gallery_access_token": "invalid_token",
                "selected": True
            }
        )

        assert response.status_code == 403

    def test_select_photo_not_found(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery: Gallery
    ):
        """Test selecting non-existent photo"""
        token_response = client.post(
            "/api/v1/auth/gallery-access",
            headers=auth_headers,
            json={"gallery_id": str(test_gallery.id)}
        )
        access_token = token_response.json()["data"]["gallery_access_token"]

        response = client.post(
            f"/api/v1/photos/{uuid4()}/select",
            json={
                "gallery_access_token": access_token,
                "selected": True
            }
        )

        assert response.status_code == 404

    def test_select_photo_missing_fields(
        self,
        client: TestClient,
        test_photo: Photo
    ):
        """Test selecting photo with missing required fields"""
        response = client.post(
            f"/api/v1/photos/{test_photo.id}/select",
            json={"selected": True}  # Missing gallery_access_token
        )

        assert response.status_code == 422


@pytest.mark.unit
class TestPhotoMetadata:
    """Tests for photo metadata and Google Drive fields"""

    def test_photo_has_google_drive_metadata(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery: Gallery,
        test_photo: Photo
    ):
        """Test that photo response includes Google Drive metadata"""
        response = client.get(
            f"/api/v1/galleries/{test_gallery.id}/photos",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        photo = data["data"][0]

        assert "google_drive_file_id" in photo
        assert "google_drive_web_view_link" in photo
        assert "google_drive_thumbnail_link" in photo
        assert "google_drive_download_link" in photo
        assert photo["google_drive_file_id"] == "drive_file_123"

    def test_photo_has_dimensions(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery: Gallery,
        test_photo: Photo
    ):
        """Test that photo includes width/height"""
        response = client.get(
            f"/api/v1/galleries/{test_gallery.id}/photos",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        photo = data["data"][0]

        assert "width" in photo
        assert "height" in photo
        assert photo["width"] == 1920
        assert photo["height"] == 1080
