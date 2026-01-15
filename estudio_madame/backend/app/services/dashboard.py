"""
Dashboard service.
"""
from typing import List, Any
from datetime import datetime

from sqlalchemy import select, func, or_
from sqlalchemy.orm import Session

from app.models.gallery import Gallery
from app.models.client import Client
from app.models.photo import Photo


class DashboardService:
    """Service for dashboard operations."""

    def __init__(self, db: Session):
        """
        Initialize the dashboard service.

        Args:
            db: Database session
        """
        self.db = db

    def get_stats(self) -> dict:
        """
        Get dashboard statistics.
        """
        # Active galleries: published or client_selection
        active_galleries = self.db.execute(
            select(func.count(Gallery.id)).where(
                Gallery.status.in_(["published", "client_selection"])
            )
        ).scalar() or 0

        # Total clients
        total_clients = self.db.execute(
            select(func.count(Client.id))
        ).scalar() or 0

        # Storage used (sum of photo sizes)
        storage_used = self.db.execute(
            select(func.sum(Photo.file_size))
        ).scalar() or 0

        # Total storage (hardcoded limit for now, e.g., 100GB)
        storage_total = 100 * 1024 * 1024 * 1024 # 100 GB

        storage_percentage = 0
        if storage_total > 0:
            storage_percentage = (storage_used / storage_total) * 100

        return {
            "active_galleries": active_galleries,
            "total_clients": total_clients,
            "storage_used_bytes": int(storage_used),
            "storage_total_bytes": storage_total,
            "storage_percentage": round(storage_percentage, 2)
        }

    def get_recent_galleries(self, limit: int = 10, status_filter: str = "all") -> List[dict]:
        """
        Get recent galleries for dashboard.
        """
        stmt = select(Gallery)

        if status_filter == "editing":
            stmt = stmt.where(Gallery.status == "draft")
        elif status_filter == "delivered":
            stmt = stmt.where(Gallery.status == "published")
        # 'all' or others: no filter

        stmt = stmt.order_by(Gallery.date_created.desc()).limit(limit)
        
        galleries = self.db.execute(stmt).scalars().all()
        
        result = []
        for g in galleries:
            # Status mapping
            dashboard_status = "Editing"
            if g.sync_status == "syncing":
                dashboard_status = "Uploading"
            elif g.status == "published":
                dashboard_status = "Delivered"
            elif g.status == "client_selection":
                dashboard_status = "Selection"
            elif g.status == "draft":
                dashboard_status = "Editing"

            # Photo count and size
            photo_stats = self.db.execute(
                select(func.count(Photo.id), func.sum(Photo.file_size))
                .where(Photo.gallery_id == g.id)
            ).first()
            
            photo_count = photo_stats[0] or 0
            total_size = photo_stats[1] or 0

            result.append({
                "id": g.id,
                "title": g.title,
                "date": g.date_created.strftime("%Y-%m-%d"),
                "image": g.cover_image,
                "status": dashboard_status,
                "photos": photo_count,
                "size": self._format_size(total_size)
            })
            
        return result

    def _format_size(self, size_bytes: int) -> str:
        """Format bytes to human readable string."""
        if size_bytes == 0:
            return "0 B"
        size_name = ("B", "KB", "MB", "GB", "TB")
        import math
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 1)
        return f"{s} {size_name[i]}"
