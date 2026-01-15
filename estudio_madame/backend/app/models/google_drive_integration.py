"""
Google Drive Integration model.
"""
import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class GoogleDriveIntegration(Base):
    __tablename__ = "google_drive_integrations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)
    access_token = Column(String, nullable=False)  # Should be encrypted
    refresh_token = Column(String, nullable=False)  # Should be encrypted
    expires_at = Column(DateTime, nullable=True)
    email = Column(String, nullable=False)
    status = Column(
        Enum("active", "expired", "disconnected", name="integration_status"),
        nullable=False,
        default="active"
    )
    connected_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_sync_at = Column(DateTime, nullable=True)
