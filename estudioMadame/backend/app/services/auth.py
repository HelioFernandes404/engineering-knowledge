"""
Authentication service for user login and token management.
"""
from datetime import datetime, timedelta
from uuid import UUID

from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User
from app.models.client import Client
from app.core.security import verify_password, get_password_hash


class AuthService:
    """Service for authentication operations."""

    def __init__(self, db: Session):
        """
        Initialize the authentication service.

        Args:
            db: Database session
        """
        self.db = db

    def authenticate_user(self, email: str, password: str) -> User | None:
        """
        Authenticate a user with email and password.

        Args:
            email: User email
            password: Plain text password

        Returns:
            User if credentials are valid, None otherwise
        """
        stmt = select(User).where(User.email == email)
        result = self.db.execute(stmt)
        user = result.scalars().first()

        if user is None:
            return None

        if not self.verify_password(password, user.hashed_password):
            return None

        return user

    def authenticate_client(self, email: str, password: str) -> Client | None:
        """
        Authenticate a client with email and password.

        Args:
            email: Client email
            password: Plain text password

        Returns:
            Client if credentials are valid, None otherwise
        """
        stmt = select(Client).where(Client.email == email)
        result = self.db.execute(stmt)
        client = result.scalars().first()

        if client is None:
            return None

        if not self.verify_password(password, client.hashed_password):
            return None

        return client

    def create_access_token(
        self,
        subject: UUID | str,
        role: str | None = None,
        expires_delta: timedelta | None = None
    ) -> str:
        """
        Create a JWT access token.

        Args:
            subject: User ID or Client ID to encode in the token
            role: Optional role to encode
            expires_delta: Optional custom expiration time

        Returns:
            Encoded JWT token
        """
        if expires_delta is None:
            expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        expire = datetime.utcnow() + expires_delta

        payload = {
            "sub": str(subject),
            "exp": expire,
            "type": "access"
        }
        
        if role:
            payload["role"] = role

        encoded_jwt = jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )

        return encoded_jwt

    def create_refresh_token(
        self,
        subject: UUID | str,
        role: str | None = None,
        expires_delta: timedelta | None = None
    ) -> str:
        """
        Create a JWT refresh token.

        Args:
            subject: User ID or Client ID to encode in the token
            role: Optional role to encode
            expires_delta: Optional custom expiration time

        Returns:
            Encoded JWT refresh token
        """
        if expires_delta is None:
            expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        expire = datetime.utcnow() + expires_delta

        payload = {
            "sub": str(subject),
            "exp": expire,
            "type": "refresh"
        }
        
        if role:
             payload["role"] = role

        encoded_jwt = jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )

        return encoded_jwt

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against a hash.
        """
        return verify_password(plain_password, hashed_password)

    def hash_password(self, password: str) -> str:
        """
        Hash a password.
        """
        return get_password_hash(password)

    def decode_token(self, token: str) -> dict:
        """
        Decode JWT token and return payload.

        Args:
            token: JWT token to decode

        Returns:
            Token payload as dictionary

        Raises:
            ValueError: If token is invalid or expired
        """
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except ExpiredSignatureError:
            raise ValueError("Token expired")
        except JWTError:
            raise ValueError("Invalid token")
