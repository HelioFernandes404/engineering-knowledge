"""
API Dependencies.
"""
from typing import Generator, Union
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.models.client import Client

# Use HTTPBearer for standard Bearer token extraction
# auto_error=False allows us to handle missing tokens with a 401 instead of 403
security = HTTPBearer(auto_error=False)


def get_token_payload(token: str) -> dict:
    """
    Decode and validate JWT token string.
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(
    db: Session = Depends(get_db),
    token_creds: HTTPAuthorizationCredentials | None = Depends(security)
) -> User:
    """
    Get the current authenticated user (Admin/Photographer).
    """
    if not token_creds:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    token = token_creds.credentials
    payload = get_token_payload(token)
    
    token_type = payload.get("type")
    if token_type and token_type != "access":
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    role = payload.get("role")
    if role == "client":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource",
        )

    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID format",
        )

    user = db.get(User, user_uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_client(
    db: Session = Depends(get_db),
    token_creds: HTTPAuthorizationCredentials | None = Depends(security)
) -> Client:
    """
    Get the current authenticated client.
    """
    if not token_creds:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = token_creds.credentials
    payload = get_token_payload(token)
    
    token_type = payload.get("type")
    if token_type and token_type != "access":
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    role = payload.get("role")
    if role != "client":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource",
        )

    client_id: str = payload.get("sub")
    if client_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    try:
        client_uuid = UUID(client_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid client ID format",
        )

    client = db.get(Client, client_uuid)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


def get_current_user_or_client(
    db: Session = Depends(get_db),
    token_creds: HTTPAuthorizationCredentials | None = Depends(security)
) -> Union[User, Client]:
    """
    Get the current authenticated entity (User or Client).
    """
    if not token_creds:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = token_creds.credentials
    payload = get_token_payload(token)
    
    token_type = payload.get("type")
    if token_type and token_type != "access":
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )

    entity_id: str = payload.get("sub")
    role = payload.get("role")
    
    if entity_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    try:
        entity_uuid = UUID(entity_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid ID format",
        )

    if role == "client":
        client = db.get(Client, entity_uuid)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        return client
    else:
        # User (Admin or Photographer)
        user = db.get(User, entity_uuid)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
