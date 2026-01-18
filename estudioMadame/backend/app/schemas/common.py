"""
Common schemas and enums.
"""
from enum import Enum
from pydantic import BaseModel, ConfigDict


class UserRole(str, Enum):
    """User role enumeration."""
    admin = "admin"
    photographer = "photographer"


class GalleryStatus(str, Enum):
    """Gallery status enumeration."""
    draft = "draft"
    published = "published"
    client_selection = "client_selection"
    archived = "archived"


class SyncStatus(str, Enum):
    """Sync status enumeration."""
    idle = "idle"
    syncing = "syncing"
    error = "error"


class ApprovalStatus(str, Enum):
    """Approval status enumeration."""
    awaiting = "awaiting"
    changes = "changes"
    complete = "complete"


class PrivacyLevel(str, Enum):
    """Gallery privacy level enumeration."""
    public = "public"
    private = "private"
    password = "password"


class GalleryLayout(str, Enum):
    """Gallery layout enumeration."""
    grid = "grid"
    masonry = "masonry"
    list = "list"


class SortOrder(str, Enum):
    """Sort order enumeration."""
    newest = "newest"
    oldest = "oldest"
    az = "az"


class PaginationMeta(BaseModel):
    """Pagination metadata."""
    page: int
    limit: int
    total: int
    total_pages: int

    model_config = ConfigDict(from_attributes=True)


class ErrorDetail(BaseModel):
    """Error detail schema."""
    code: str
    message: str
    details: dict | None = None

    model_config = ConfigDict(from_attributes=True)
