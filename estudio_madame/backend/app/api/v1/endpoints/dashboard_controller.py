"""
Dashboard controller.
"""
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api import deps
from app.services.dashboard import DashboardService

router = APIRouter(prefix="/api/v1/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=dict)
def get_stats(
    db: Session = Depends(get_db),
    current_user: deps.User = Depends(deps.get_current_user)
):
    """
    Obter estatísticas do dashboard.
    """
    dashboard_service = DashboardService(db)
    stats = dashboard_service.get_stats()
    
    return {
        "data": stats
    }


@router.get("/recent-galleries", response_model=dict)
def get_recent_galleries(
    limit: int = Query(10, ge=1, le=50),
    status_filter: str = Query("all"),
    db: Session = Depends(get_db),
    current_user: deps.User = Depends(deps.get_current_user)
):
    """
    Listar galerias recentes para o dashboard.
    """
    dashboard_service = DashboardService(db)
    galleries = dashboard_service.get_recent_galleries(limit=limit, status_filter=status_filter)
    
    return {
        "data": galleries
    }
