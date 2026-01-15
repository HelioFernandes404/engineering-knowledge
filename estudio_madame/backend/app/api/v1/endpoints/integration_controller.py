"""
Google Drive Integration controller.
"""
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api import deps
from app.models.google_drive_integration import GoogleDriveIntegration
from app.services.google_drive import GoogleDriveService

router = APIRouter(prefix="/api/v1/integrations/google-drive", tags=["Integrations"])


@router.get("/auth-url", response_model=dict)
def get_auth_url(
    db: Session = Depends(get_db),
    current_user: deps.User = Depends(deps.get_current_user)
):
    """
    Obter URL de autenticação do Google Drive.
    """
    drive_service = GoogleDriveService(db)
    auth_url = drive_service.get_auth_url()
    
    return {
        "data": {
            "auth_url": auth_url
        }
    }


@router.post("/callback", response_model=dict)
def oauth_callback(
    request: dict,
    db: Session = Depends(get_db),
    current_user: deps.User = Depends(deps.get_current_user)
):
    """
    Callback OAuth2 do Google Drive.
    """
    code = request.get("code")
    if not code:
        raise HTTPException(status_code=422, detail="Missing authorization code")
        
    drive_service = GoogleDriveService(db)
    try:
        tokens = drive_service.exchange_code_for_tokens(code)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    # Upsert integration
    integration = drive_service.get_user_integration(current_user.id)
    if not integration:
        integration = GoogleDriveIntegration(
            user_id=current_user.id,
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            email=tokens["email"],
            status="active"
        )
        db.add(integration)
    else:
        integration.access_token = tokens["access_token"]
        if "refresh_token" in tokens:
            integration.refresh_token = tokens["refresh_token"]
        integration.email = tokens["email"]
        integration.status = "active"
        
    db.commit()
    db.refresh(integration)
    
    return {
        "data": {
            "id": integration.id,
            "user_id": integration.user_id,
            "email": integration.email,
            "status": integration.status,
            "connected_at": integration.connected_at
        }
    }


@router.get("/status", response_model=dict)
def get_status(
    db: Session = Depends(get_db),
    current_user: deps.User = Depends(deps.get_current_user)
):
    """
    Verificar status da integração Google Drive.
    """
    drive_service = GoogleDriveService(db)
    integration = drive_service.get_user_integration(current_user.id)
    
    if not integration:
        return {
            "data": None
        }
        
    return {
        "data": {
            "id": integration.id,
            "user_id": integration.user_id,
            "email": integration.email,
            "status": integration.status,
            "connected_at": integration.connected_at,
            "last_sync_at": integration.last_sync_at
        }
    }


@router.delete("/disconnect", status_code=status.HTTP_204_NO_CONTENT)
def disconnect(
    db: Session = Depends(get_db),
    current_user: deps.User = Depends(deps.get_current_user)
):
    """
    Desconectar Google Drive.
    """
    drive_service = GoogleDriveService(db)
    success = drive_service.revoke_tokens(current_user.id)
    
    if not success:
        # Handle gracefully if not found
        return


@router.get("/folders", response_model=dict)
def list_folders(
    parent_id: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: deps.User = Depends(deps.get_current_user)
):
    """
    Listar pastas do Google Drive.
    """
    drive_service = GoogleDriveService(db)
    integration = drive_service.get_user_integration(current_user.id)
    
    if not integration:
        raise HTTPException(status_code=400, detail="Google Drive not connected")
        
    if integration.status != "active":
         raise HTTPException(status_code=400, detail=f"Integration status is {integration.status}")

    try:
        folders = drive_service.list_folders(parent_id=parent_id, search=search)
    except Exception as e:
        if "Token expired" in str(e):
             raise HTTPException(status_code=401, detail="Google Drive token expired")
        raise HTTPException(status_code=400, detail=str(e))
        
    return {
        "data": folders
    }
