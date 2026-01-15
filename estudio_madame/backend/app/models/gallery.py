"""
Gallery model.
"""
import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer, Boolean, Enum, ForeignKey, JSON, Date
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class Gallery(Base):
    __tablename__ = "galleries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    status = Column(
        Enum("draft", "published", "client_selection", "archived", name="gallery_status"),
        nullable=False,
        default="draft"
    )
    cover_image = Column(String, nullable=True)
    event_date = Column(Date, nullable=True)
    location = Column(String, nullable=True)
    access_token = Column(String, nullable=True)

    # Google Drive integration
    google_drive_folder_id = Column(String, nullable=True)
    google_drive_folder_name = Column(String, nullable=True)
    auto_sync_enabled = Column(Boolean, default=False, nullable=False)
    last_sync_at = Column(DateTime, nullable=True)
    sync_status = Column(
        Enum("idle", "syncing", "error", name="sync_status"),
        nullable=False,
        default="idle"
    )

    # Settings stored as JSON
    settings = Column(JSON, nullable=True)

    # Timestamps
    date_created = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
