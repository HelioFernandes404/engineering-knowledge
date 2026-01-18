"""
Authentication endpoints.
"""
import secrets
from uuid import UUID
from datetime import datetime, timedelta
from typing import Union

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app.models.user import User as UserModel
from app.models.client import Client as ClientModel
from app.models.gallery import Gallery
from app.schemas.user import (
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    User
)
from app.schemas.client import (
    ClientLoginRequest,
    ClientLoginResponse,
    Client as ClientSchema
)
from app.schemas.gallery import (
    GalleryAccessTokenRequest,
    GalleryAccessTokenResponse,
    Gallery as GallerySchema
)
from app.services.auth import AuthService
from app.api import deps

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/login", response_model=dict)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    User Login endpoint.
    """
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(request.email, request.password)
    if user is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Invalid email or password"}
        )

    access_token = auth_service.create_access_token(user.id, role=user.role)
    refresh_token = auth_service.create_refresh_token(user.id, role=user.role)
    expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    user_data = User.model_validate(user)

    return {"data": LoginResponse(
        user=user_data,
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=expires_in
    ).model_dump()}


@router.post("/client/login", response_model=dict)
async def client_login(
    request: ClientLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Client Login endpoint.
    """
    auth_service = AuthService(db)
    client = auth_service.authenticate_client(request.email, request.password)
    if client is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Invalid email or password"}
        )

    access_token = auth_service.create_access_token(client.id, role="client")
    refresh_token = auth_service.create_refresh_token(client.id, role="client")
    expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    
    client_data = ClientSchema.model_validate(client)
    client_data.galleries_count = 0 
    client_data.last_activity = None
    
    return {"data": ClientLoginResponse(
        client=client_data,
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=expires_in
    ).model_dump()}


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    token_creds: HTTPAuthorizationCredentials | None = Depends(deps.security)
):
    """
    Logout endpoint.
    """
    if not token_creds:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    
    # Validate token to ensure 401 if invalid
    deps.get_token_payload(token_creds.credentials)
    
    return


@router.post("/gallery-access", response_model=dict)
async def gallery_access(
    request: GalleryAccessTokenRequest,
    db: Session = Depends(get_db),
    current_entity: Union[UserModel, ClientModel] = Depends(deps.get_current_user_or_client)
):
    """
    Generate/Retrieve access token for gallery viewing.
    """
    stmt = select(Gallery).where(Gallery.id == request.gallery_id)
    result = db.execute(stmt)
    gallery = result.scalars().first()
    
    if not gallery:
        raise HTTPException(status_code=404, detail="Gallery not found")

    # If the user is a client, ensure they own the gallery
    if isinstance(current_entity, ClientModel):
        if gallery.client_id != current_entity.id:
             raise HTTPException(status_code=403, detail="Not authorized for this gallery")
        
    settings_dict = gallery.settings or {}
    privacy = settings_dict.get("privacy", "private")
    stored_password = settings_dict.get("password")
    
    if privacy == "password":
        if not request.password or request.password != stored_password:
             raise HTTPException(status_code=403, detail="Invalid password")
            
    token = gallery.access_token
    if not token:
        token = secrets.token_urlsafe(16)
        gallery.access_token = token
        db.commit()
        
    response = GalleryAccessTokenResponse(
        gallery_access_token=token,
        gallery_id=gallery.id,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )
    
    return {"data": response.model_dump()}


@router.post("/verify-gallery-access", response_model=dict)
async def verify_gallery_access(
    request: dict,
    db: Session = Depends(get_db)
):
    """
    Verify gallery access token.
    """
    token = request.get("gallery_access_token")
    gallery_id_str = request.get("gallery_id")
    
    if not token or not gallery_id_str:
        raise HTTPException(status_code=422, detail="Missing fields")
        
    try:
        gallery_id = UUID(gallery_id_str)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid gallery ID format")

    stmt = select(Gallery).where(
        Gallery.id == gallery_id,
        Gallery.access_token == token
    )
    gallery = db.execute(stmt).scalar_one_or_none()
    
    if not gallery:
        raise HTTPException(status_code=403, detail="Invalid token")
        
    # Enrich to satisfy GallerySchema
    client = db.get(ClientModel, gallery.client_id)
    gallery.client_name = client.name if client else "Unknown"
    
    from app.services.gallery import GalleryService
    gallery_service = GalleryService(db)
    gallery.photo_count = gallery_service.get_photo_count(gallery.id)
        
    return {
        "data": {
            "valid": True,
            "gallery": GallerySchema.model_validate(gallery).model_dump()
        }
    }


@router.post("/refresh", response_model=dict)
async def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh token endpoint.

    Generates a new access token using a valid refresh token.
    Supports both User and Client tokens.
    """
    auth_service = AuthService(db)

    # Decode and validate refresh token
    try:
        payload = auth_service.decode_token(request.refresh_token)
    except ValueError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Invalid or expired refresh token"}
        )

    # Verify token type is refresh
    if payload.get("type") != "refresh":
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Invalid token type"}
        )

    # Get user/client ID and role from payload
    user_id = payload.get("sub")
    role = payload.get("role", "user") # Default to user for legacy tokens

    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Invalid token payload"}
        )

    try:
        user_uuid = UUID(user_id)
    except (ValueError, AttributeError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Invalid user ID"}
        )

    # Verify entity still exists
    if role == "client":
        stmt = select(ClientModel).where(ClientModel.id == user_uuid)
    else:
        stmt = select(UserModel).where(UserModel.id == user_uuid)
        
    result = db.execute(stmt)
    entity = result.scalars().first()

    if entity is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "User/Client not found"}
        )

    # Generate new access token
    access_token = auth_service.create_access_token(entity.id, role=role)

    # Calculate expires_in (in seconds)
    expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60

    # Create response
    refresh_response = RefreshTokenResponse(
        access_token=access_token,
        expires_in=expires_in
    )

    # Wrap in data envelope as expected by tests
    return {"data": refresh_response.model_dump()}