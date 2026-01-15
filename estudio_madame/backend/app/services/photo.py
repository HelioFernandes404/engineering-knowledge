"""
Photo service.
"""
from typing import List, Optional, Tuple
from uuid import UUID

from sqlalchemy import select, func, and_
from sqlalchemy.orm import Session

from app.services.base import BaseService
from app.models.photo import Photo
from app.models.gallery import Gallery


class PhotoService(BaseService[Photo]):
    """Service for photo operations."""

    def __init__(self, db: Session):
        """
        Initialize the photo service.

        Args:
            db: Database session
        """
        super().__init__(db, Photo)

    def list_photos(
        self,
        gallery_id: UUID,
        page: int = 1,
        limit: int = 50,
        selected_by_client: Optional[bool] = None
    ) -> Tuple[List[Photo], int]:
        """
        List photos in a gallery with filters and pagination.
        """
        stmt = select(Photo).where(Photo.gallery_id == gallery_id)

        if selected_by_client is not None:
            stmt = stmt.where(Photo.selected_by_client == selected_by_client)

        # Count total
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = self.db.execute(count_stmt).scalar() or 0

        # Pagination
        offset = (page - 1) * limit
        stmt = stmt.offset(offset).limit(limit)

        # Execute
        result = self.db.execute(stmt)
        photos = result.scalars().all()

        return list(photos), total

    def toggle_selection(
        self,
        photo_id: UUID,
        selected: bool,
        gallery_id: UUID
    ) -> Optional[Photo]:
        """
        Toggle client selection for a photo.
        """
        # Ensure photo belongs to gallery
        stmt = select(Photo).where(
            and_(
                Photo.id == photo_id,
                Photo.gallery_id == gallery_id
            )
        )
        photo = self.db.execute(stmt).scalar_one_or_none()
        
        if not photo:
            return None

        # Check selection limit if selecting
        if selected:
            gallery_stmt = select(Gallery).where(Gallery.id == gallery_id)
            gallery = self.db.execute(gallery_stmt).scalar_one_or_none()
            
            if gallery and gallery.settings:
                max_selection = gallery.settings.get("max_client_selection")
                if max_selection:
                    current_count = self.get_selected_count(gallery_id)
                    if current_count >= max_selection:
                        # Limit reached
                        return None

        photo.selected_by_client = selected
        self.db.commit()
        self.db.refresh(photo)
        return photo

    def get_selected_count(self, gallery_id: UUID) -> int:
        """
        Get count of selected photos in a gallery.
        """
        stmt = select(func.count(Photo.id)).where(
            and_(
                Photo.gallery_id == gallery_id,
                Photo.selected_by_client == True
            )
        )
        return self.db.execute(stmt).scalar() or 0
