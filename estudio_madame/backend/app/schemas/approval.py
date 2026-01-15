"""
Approval schemas.
"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.common import ApprovalStatus


class ApprovalBase(BaseModel):
    """Base approval schema."""
    gallery_id: UUID
    gallery_name: str
    client_id: UUID
    client_name: str


class ApprovalCreate(ApprovalBase):
    """Schema for creating an approval."""
    selected_count: int = 0
    total_count: int = 0


class ApprovalUpdate(BaseModel):
    """Schema for updating an approval."""
    status: ApprovalStatus | None = None
    selected_count: int | None = None
    total_count: int | None = None


class Approval(ApprovalBase):
    """Approval schema for API responses."""
    id: UUID
    client_avatar: str | None = None
    status: ApprovalStatus
    selected_count: int
    total_count: int
    submitted_at: datetime | None = None
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ApprovalInDB(ApprovalBase):
    """Approval schema as stored in database."""
    id: UUID
    status: ApprovalStatus
    selected_count: int
    total_count: int
    submitted_at: datetime | None = None
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ApprovalSubmitRequest(BaseModel):
    """Approval submission request schema."""
    gallery_access_token: str


class ApprovalSubmitResponse(BaseModel):
    """Approval submission response schema."""
    approval_id: UUID
    status: ApprovalStatus
    submitted_at: datetime
