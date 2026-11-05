import os
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from urllib.parse import urlsplit

import httpx
import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app import models  # noqa: F401
from app.core.security import create_access_token
from app.database.base import Base
from app.database.database import DATABASE_URL, get_db
from app.main import app


def _test_database_url():
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        pytest.fail("Set TEST_DATABASE_URL to run PostgreSQL integration tests")
    if not url.startswith(("postgresql+asyncpg://", "postgresql://")):
        pytest.fail("TEST_DATABASE_URL must use PostgreSQL")

    def identity(value):
        parsed = urlsplit(value.replace("postgresql://", "postgresql+asyncpg://", 1))
        return parsed.hostname, parsed.port or 5432, parsed.path.lstrip("/")

    if identity(url) == identity(DATABASE_URL):
        pytest.fail("TEST_DATABASE_URL points at the configured application database")
    return url.replace("postgresql://", "postgresql+asyncpg://", 1)


@pytest.fixture
def test_database_url():
    return _test_database_url()


@pytest.fixture
async def db_engine(test_database_url):

    engine = create_async_engine(test_database_url)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def db_session(db_engine):

    factory = async_sessionmaker(db_engine, expire_on_commit=False)
    async with factory() as session:
        yield session


@pytest.fixture
def api_app():

    return app


@pytest.fixture
async def api_client(api_app):

    async def fake_db():
        yield object()

    api_app.dependency_overrides[get_db] = fake_db
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=api_app), base_url="http://test"
    ) as client:
        yield client
    api_app.dependency_overrides.clear()


@pytest.fixture
def sample_admin():

    return SimpleNamespace(id=1, role="admin", is_active=True)


@pytest.fixture
def sample_lineman():

    return SimpleNamespace(id=2, role="lineman", is_active=True)


@pytest.fixture
def sample_customer():

    return SimpleNamespace(id=3, email="customer@example.com", is_active=True)


@pytest.fixture
def access_token():

    return create_access_token(1, "employee", "admin")


@pytest.fixture
def mock_repository():

    repository = MagicMock()
    for method in (
        "get_employee_by_email",
        "get_employee_by_username",
        "get_employee_by_id",
        "create_employee",
        "deactivate_employee",
        "get_customer_by_email",
        "get_customer_by_username",
        "get_customer_by_id",
        "create_customer",
        "deactivate_customer",
        "create_complaint",
        "get_complaint_by_id",
        "assign_complaint",
        "close_complaint",
        "update_complaint",
        "update_complaint_image",
        "get_assignment",
        "get_repair_by_complaint_id",
        "create_repair",
        "update_repair_image",
    ):
        setattr(repository, method, AsyncMock())
    return repository


@pytest.fixture
def mock_external_operations(monkeypatch):

    email = MagicMock()
    upload = AsyncMock(return_value="/tmp/test-upload.png")
    monkeypatch.setattr(
        "app.services.implementations.complaint_service.send_complaint_registered_email",
        email,
    )
    monkeypatch.setattr(
        "app.services.implementations.complaint_service.send_complaint_closed_email",
        email,
    )
    monkeypatch.setattr(
        "app.services.implementations.complaint_service.upload_image", upload
    )
    monkeypatch.setattr(
        "app.services.implementations.repair_service.upload_image", upload
    )
    return {"email": email, "upload": upload}
