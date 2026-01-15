"""
Pytest configuration and shared fixtures for all tests.
"""
import pytest
from typing import Generator, AsyncGenerator
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app
from app.core.config import settings
from app.models.user import User
from app.models.client import Client
from app.models.gallery import Gallery
from app.core.security import get_password_hash, create_access_token


# Test database setup
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """
    Create a fresh database for each test.
    """
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    """
    Create a TestClient with the test database.
    """
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
async def async_client(db: Session) -> AsyncGenerator[AsyncClient, None]:
    """
    Create an AsyncClient for async tests.
    """
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db: Session) -> User:
    """
    Create a test admin user.
    """
    user = User(
        email="admin@test.com",
        name="Test Admin",
        role="admin",
        hashed_password=get_password_hash("test123")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_photographer(db: Session) -> User:
    """
    Create a test photographer user.
    """
    user = User(
        email="photographer@test.com",
        name="Test Photographer",
        role="photographer",
        hashed_password=get_password_hash("test123")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_client_model(db: Session) -> Client:
    """
    Create a test client.
    """
    client = Client(
        name="John Doe",
        email="john@example.com",
        hashed_password=get_password_hash("client123"),
        phone="+1234567890"
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


@pytest.fixture
def test_gallery(db: Session, test_client_model: Client) -> Gallery:
    """
    Create a test gallery.
    """
    gallery = Gallery(
        title="Test Wedding Gallery",
        description="Beautiful wedding photos",
        client_id=test_client_model.id,
        status="published",
        auto_sync_enabled=False
    )
    db.add(gallery)
    db.commit()
    db.refresh(gallery)
    return gallery


@pytest.fixture
def admin_token(test_user: User) -> str:
    """
    Generate a valid JWT token for admin user.
    """
    return create_access_token(
        data={"sub": str(test_user.id), "role": "admin"}
    )


@pytest.fixture
def photographer_token(test_photographer: User) -> str:
    """
    Generate a valid JWT token for photographer user.
    """
    return create_access_token(
        data={"sub": str(test_photographer.id), "role": "photographer"}
    )


@pytest.fixture
def auth_headers(admin_token: str) -> dict:
    """
    Create authorization headers with admin token.
    """
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def photographer_headers(photographer_token: str) -> dict:
    """
    Create authorization headers with photographer token.
    """
    return {"Authorization": f"Bearer {photographer_token}"}