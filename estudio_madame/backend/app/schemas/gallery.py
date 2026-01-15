"""
Gallery schemas.
"""
from datetime import datetime, date
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.common import GalleryStatus, SyncStatus, PrivacyLevel, GalleryLayout, SortOrder


class GallerySettings(BaseModel):
    """Gallery settings schema."""
    privacy: PrivacyLevel = PrivacyLevel.private
    password: str | None = None
    allow_downloads: bool = True
    mature_content: bool = False
    max_client_selection: int | None = None
    layout: GalleryLayout = GalleryLayout.grid
    default_sort: SortOrder = SortOrder.newest

    model_config = ConfigDict(from_attributes=True)


class GalleryStats(BaseModel):
    """Gallery statistics schema."""
    views: int = 0
    downloads: int = 0
    selections: int = 0

    model_config = ConfigDict(from_attributes=True)


class GalleryBase(BaseModel):
    """Base gallery schema."""
    title: str
    description: str | None = None


class GalleryCreate(GalleryBase):
    """Schema for creating a gallery."""
    client_id: UUID
    event_date: date | None = None
    location: str | None = None
    cover_image: str | None = None
    google_drive_folder_id: str | None = None
    auto_sync_enabled: bool = False
    settings: GallerySettings | None = None


class GalleryUpdate(BaseModel):
    """Schema for updating a gallery."""
    title: str | None = None
    description: str | None = None
    status: GalleryStatus | None = None
    event_date: date | None = None
    location: str | None = None
    cover_image: str | None = None
    auto_sync_enabled: bool | None = None
    settings: GallerySettings | None = None


class Gallery(GalleryBase):
    """Gallery schema for API responses."""
    id: UUID
    client_id: UUID
    client_name: str
    status: GalleryStatus
    cover_image: str | None = None
    photo_count: int = 0
    date_created: datetime
    event_date: date | None = None
    location: str | None = None
    access_token: str | None = None
    google_drive_folder_id: str | None = None
    google_drive_folder_name: str | None = None
    auto_sync_enabled: bool
    last_sync_at: datetime | None = None
    sync_status: SyncStatus
    settings: GallerySettings | None = None
    stats: GalleryStats | None = None

    model_config = ConfigDict(from_attributes=True)


class GalleryInDB(GalleryBase):
    """Gallery schema as stored in database."""
    id: UUID
    client_id: UUID
    status: GalleryStatus
    cover_image: str | None = None
    event_date: date | None = None
    location: str | None = None
    access_token: str | None = None
    google_drive_folder_id: str | None = None
    google_drive_folder_name: str | None = None
    auto_sync_enabled: bool
    last_sync_at: datetime | None = None
    sync_status: SyncStatus
    settings: dict | None = None
    date_created: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class GalleryPublic(BaseModel):
    """Public gallery schema for client viewing."""
    id: UUID
    title: str
    description: str | None = None
    event_date: date | None = None
    location: str | None = None
    photo_count: int
    settings: GallerySettings | None = None

    model_config = ConfigDict(from_attributes=True)


class BulkActionRequest(BaseModel):
    """Bulk action request schema."""
    action: str  # delete, change_status, share
    gallery_ids: list[UUID]
    params: dict | None = None


class BulkActionResponse(BaseModel):
    """Bulk action response schema."""
    success_count: int
    failed_count: int
    errors: list[dict] = []


class SyncJobResponse(BaseModel):
    """Sync job response schema."""
    sync_job_id: UUID
    status: str
    started_at: datetime


class GalleryAccessTokenRequest(BaseModel):
    """Gallery access token request schema."""
    gallery_id: UUID
    password: str | None = None


class GalleryAccessTokenResponse(BaseModel):
    """Gallery access token response schema."""
    gallery_access_token: str
    gallery_id: UUID
    expires_at: datetime
