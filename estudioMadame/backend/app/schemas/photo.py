"""
Photo schemas.
"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PhotoMetadata(BaseModel):
    """Photo metadata schema."""
    camera: str | None = None
    lens: str | None = None
    exif: dict | None = None

    model_config = ConfigDict(from_attributes=True)


class PhotoBase(BaseModel):
    """Base photo schema."""
    file_name: str
    google_drive_file_id: str


class PhotoCreate(PhotoBase):
    """Schema for creating a photo."""
    gallery_id: UUID
    google_drive_web_view_link: str | None = None
    google_drive_thumbnail_link: str | None = None
    google_drive_download_link: str | None = None
    file_size: int
    mime_type: str
    width: int | None = None
    height: int | None = None
    created_in_drive: datetime | None = None
    metadata: PhotoMetadata | None = None


class PhotoUpdate(BaseModel):
    """Schema for updating a photo."""
    google_drive_web_view_link: str | None = None
    google_drive_thumbnail_link: str | None = None
    google_drive_download_link: str | None = None
    selected_by_client: bool | None = None
    metadata: PhotoMetadata | None = None


class Photo(PhotoBase):
    """Photo schema for API responses."""
    id: UUID
    gallery_id: UUID
    google_drive_web_view_link: str | None = None
    google_drive_thumbnail_link: str | None = None
    google_drive_download_link: str | None = None
    file_size: int
    mime_type: str
    width: int | None = None
    height: int | None = None
    selected_by_client: bool = False
    created_in_drive: datetime | None = None
    synced_at: datetime
    metadata: PhotoMetadata | None = Field(None, alias='photo_metadata')

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PhotoInDB(PhotoBase):
    """Photo schema as stored in database."""
    id: UUID
    gallery_id: UUID
    google_drive_web_view_link: str | None = None
    google_drive_thumbnail_link: str | None = None
    google_drive_download_link: str | None = None
    file_size: int
    mime_type: str
    width: int | None = None
    height: int | None = None
    selected_by_client: bool
    photo_metadata: dict | None = None
    created_in_drive: datetime | None = None
    synced_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PhotoSelectRequest(BaseModel):
    """Photo selection request schema."""
    gallery_access_token: str
    selected: bool


class PhotoSelectResponse(BaseModel):
    """Photo selection response schema."""
    photo_id: UUID
    selected: bool
    current_selection_count: int
