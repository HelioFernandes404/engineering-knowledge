"""
Approval model.
"""
import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class Approval(Base):
    __tablename__ = "approvals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    gallery_id = Column(UUID(as_uuid=True), ForeignKey("galleries.id"), nullable=False)
    gallery_name = Column(String, nullable=False)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    client_name = Column(String, nullable=False)
    status = Column(
        Enum("awaiting", "changes", "complete", name="approval_status"),
        nullable=False,
        default="awaiting"
    )
    selected_count = Column(Integer, default=0, nullable=False)
    total_count = Column(Integer, default=0, nullable=False)
    submitted_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
