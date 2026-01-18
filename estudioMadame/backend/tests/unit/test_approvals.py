"""
Unit tests for Approvals endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from uuid import uuid4

from app.models.approval import Approval
from app.models.gallery import Gallery
from app.models.client import Client


@pytest.fixture
def test_approval(
    db: Session,
    test_gallery: Gallery,
    test_client_model: Client
) -> Approval:
    """Create a test approval"""
    approval = Approval(
        gallery_id=test_gallery.id,
        gallery_name=test_gallery.title,
        client_id=test_client_model.id,
        client_name=test_client_model.name,
        status="awaiting",
        selected_count=0,
        total_count=100
    )
    db.add(approval)
    db.commit()
    db.refresh(approval)
    return approval


@pytest.mark.unit
class TestListApprovals:
    """Tests for GET /api/v1/approvals"""

    def test_list_approvals_success(
        self,
        client: TestClient,
        auth_headers: dict,
        test_approval: Approval
    ):
        """Test listing all approvals"""
        response = client.get(
            "/api/v1/approvals",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "meta" in data
        assert isinstance(data["data"], list)
        assert len(data["data"]) >= 1

    def test_list_approvals_with_pagination(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test approvals pagination"""
        response = client.get(
            "/api/v1/approvals?page=1&limit=20",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["meta"]["page"] == 1
        assert data["meta"]["limit"] == 20

    def test_list_approvals_filter_by_status(
        self,
        client: TestClient,
        auth_headers: dict,
        test_approval: Approval
    ):
        """Test filtering approvals by status"""
        response = client.get(
            "/api/v1/approvals?status=awaiting",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        for approval in data["data"]:
            assert approval["status"] == "awaiting"

    def test_list_approvals_search(
        self,
        client: TestClient,
        auth_headers: dict,
        test_approval: Approval
    ):
        """Test searching approvals by client or gallery name"""
        response = client.get(
            f"/api/v1/approvals?search=John",
            headers=auth_headers
        )

        assert response.status_code == 200

    def test_list_approvals_unauthorized(self, client: TestClient):
        """Test listing approvals without authentication"""
        response = client.get("/api/v1/approvals")

        assert response.status_code == 401


@pytest.mark.unit
class TestGetApproval:
    """Tests for GET /api/v1/approvals/{id}"""

    def test_get_approval_success(
        self,
        client: TestClient,
        auth_headers: dict,
        test_approval: Approval
    ):
        """Test getting approval details"""
        response = client.get(
            f"/api/v1/approvals/{test_approval.id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["id"] == str(test_approval.id)
        assert data["data"]["gallery_name"] == test_approval.gallery_name
        assert data["data"]["client_name"] == test_approval.client_name
        assert data["data"]["status"] == "awaiting"
        assert "selected_count" in data["data"]
        assert "total_count" in data["data"]

    def test_get_approval_not_found(
        self,
        client: TestClient,
        auth_headers: dict
    ):
        """Test getting non-existent approval"""
        response = client.get(
            f"/api/v1/approvals/{uuid4()}",
            headers=auth_headers
        )

        assert response.status_code == 404

    def test_get_approval_unauthorized(
        self,
        client: TestClient,
        test_approval: Approval
    ):
        """Test getting approval without authentication"""
        response = client.get(f"/api/v1/approvals/{test_approval.id}")

        assert response.status_code == 401


@pytest.mark.unit
class TestSubmitApproval:
    """Tests for POST /api/v1/approvals/{id}/submit"""

    def test_submit_approval_success(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery: Gallery,
        test_approval: Approval,
        db: Session
    ):
        """Test client submitting approval"""
        # Generate gallery access token
        token_response = client.post(
            "/api/v1/auth/gallery-access",
            headers=auth_headers,
            json={"gallery_id": str(test_gallery.id)}
        )
        access_token = token_response.json()["data"]["gallery_access_token"]

        # Submit approval
        response = client.post(
            f"/api/v1/approvals/{test_approval.id}/submit",
            json={"gallery_access_token": access_token}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["approval_id"] == str(test_approval.id)
        assert "status" in data["data"]
        assert "submitted_at" in data["data"]

    def test_submit_approval_updates_status(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery: Gallery,
        test_approval: Approval
    ):
        """Test that submitting approval updates its status"""
        # Generate token
        token_response = client.post(
            "/api/v1/auth/gallery-access",
            headers=auth_headers,
            json={"gallery_id": str(test_gallery.id)}
        )
        access_token = token_response.json()["data"]["gallery_access_token"]

        # Submit
        response = client.post(
            f"/api/v1/approvals/{test_approval.id}/submit",
            json={"gallery_access_token": access_token}
        )

        assert response.status_code == 200

        # Verify status changed
        get_response = client.get(
            f"/api/v1/approvals/{test_approval.id}",
            headers=auth_headers
        )
        data = get_response.json()
        assert data["data"]["status"] in ["changes", "complete"]

    def test_submit_approval_invalid_token(
        self,
        client: TestClient,
        test_approval: Approval
    ):
        """Test submitting approval with invalid token"""
        response = client.post(
            f"/api/v1/approvals/{test_approval.id}/submit",
            json={"gallery_access_token": "invalid_token"}
        )

        assert response.status_code == 403

    def test_submit_approval_not_found(
        self,
        client: TestClient,
        auth_headers: dict,
        test_gallery: Gallery
    ):
        """Test submitting non-existent approval"""
        token_response = client.post(
            "/api/v1/auth/gallery-access",
            headers=auth_headers,
            json={"gallery_id": str(test_gallery.id)}
        )
        access_token = token_response.json()["data"]["gallery_access_token"]

        response = client.post(
            f"/api/v1/approvals/{uuid4()}/submit",
            json={"gallery_access_token": access_token}
        )

        assert response.status_code == 404

    def test_submit_approval_missing_token(
        self,
        client: TestClient,
        test_approval: Approval
    ):
        """Test submitting approval without token"""
        response = client.post(
            f"/api/v1/approvals/{test_approval.id}/submit",
            json={}
        )

        assert response.status_code == 422


@pytest.mark.unit
class TestApprovalStatuses:
    """Tests for different approval statuses"""

    def test_approval_status_awaiting(
        self,
        client: TestClient,
        auth_headers: dict,
        db: Session,
        test_gallery: Gallery,
        test_client_model: Client
    ):
        """Test approval with awaiting status"""
        approval = Approval(
            gallery_id=test_gallery.id,
            gallery_name=test_gallery.title,
            client_id=test_client_model.id,
            client_name=test_client_model.name,
            status="awaiting",
            selected_count=0,
            total_count=100
        )
        db.add(approval)
        db.commit()

        response = client.get(
            f"/api/v1/approvals/{approval.id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["status"] == "awaiting"
        assert data["data"]["selected_count"] == 0

    def test_approval_status_changes(
        self,
        client: TestClient,
        auth_headers: dict,
        db: Session,
        test_gallery: Gallery,
        test_client_model: Client
    ):
        """Test approval with changes status"""
        approval = Approval(
            gallery_id=test_gallery.id,
            gallery_name=test_gallery.title,
            client_id=test_client_model.id,
            client_name=test_client_model.name,
            status="changes",
            selected_count=50,
            total_count=100
        )
        db.add(approval)
        db.commit()

        response = client.get(
            f"/api/v1/approvals/{approval.id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["status"] == "changes"

    def test_approval_status_complete(
        self,
        client: TestClient,
        auth_headers: dict,
        db: Session,
        test_gallery: Gallery,
        test_client_model: Client
    ):
        """Test approval with complete status"""
        approval = Approval(
            gallery_id=test_gallery.id,
            gallery_name=test_gallery.title,
            client_id=test_client_model.id,
            client_name=test_client_model.name,
            status="complete",
            selected_count=85,
            total_count=200
        )
        db.add(approval)
        db.commit()

        response = client.get(
            f"/api/v1/approvals/{approval.id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["status"] == "complete"
        assert data["data"]["selected_count"] == 85


@pytest.mark.unit
class TestApprovalMetadata:
    """Tests for approval metadata fields"""

    def test_approval_has_client_avatar(
        self,
        client: TestClient,
        auth_headers: dict,
        test_approval: Approval
    ):
        """Test that approval includes client avatar"""
        response = client.get(
            f"/api/v1/approvals/{test_approval.id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "client_avatar" in data["data"]

    def test_approval_has_timestamps(
        self,
        client: TestClient,
        auth_headers: dict,
        test_approval: Approval
    ):
        """Test that approval has submitted_at and updated_at"""
        response = client.get(
            f"/api/v1/approvals/{test_approval.id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "updated_at" in data["data"]
        assert "submitted_at" in data["data"]

    def test_approval_selection_progress(
        self,
        client: TestClient,
        auth_headers: dict,
        db: Session,
        test_gallery: Gallery,
        test_client_model: Client
    ):
        """Test approval shows selection progress correctly"""
        approval = Approval(
            gallery_id=test_gallery.id,
            gallery_name=test_gallery.title,
            client_id=test_client_model.id,
            client_name=test_client_model.name,
            status="changes",
            selected_count=75,
            total_count=150
        )
        db.add(approval)
        db.commit()

        response = client.get(
            f"/api/v1/approvals/{approval.id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["selected_count"] == 75
        assert data["data"]["total_count"] == 150
