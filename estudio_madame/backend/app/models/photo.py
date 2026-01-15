"""
Photo model.
"""
import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer, Boolean, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class Photo(Base):
    __tablename__ = "photos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    gallery_id = Column(UUID(as_uuid=True), ForeignKey("galleries.id"), nullable=False)

    # Google Drive metadata
    google_drive_file_id = Column(String, nullable=False, unique=True)
    google_drive_web_view_link = Column(String, nullable=True)
    google_drive_thumbnail_link = Column(String, nullable=True)
    google_drive_download_link = Column(String, nullable=True)

    # File info
    file_name = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String, nullable=False)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)

    # Selection
    selected_by_client = Column(Boolean, default=False, nullable=False)

    # Metadata
    photo_metadata = Column(JSON, nullable=True)

    # Timestamps
    created_in_drive = Column(DateTime, nullable=True)
    synced_at = Column(DateTime, default=datetime.utcnow, nullable=False)
