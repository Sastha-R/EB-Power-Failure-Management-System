import pytest
from fastapi import FastAPI
from httpx import AsyncClient, Response

from app.api.dependencies.auth_service_dependency import get_auth_service


@pytest.mark.api
@pytest.mark.asyncio
async def test_login_endpoint_returns_tokens(
    api_app: FastAPI, api_client: AsyncClient
) -> None:
    class Service:
        async def employee_login(
            self, db: object, username: str, password: str
        ) -> dict[str, str]:
            assert username == "admin@example.com"
            return {
                "access_token": "access",
                "refresh_token": "refresh",
                "token_type": "bearer",
            }

    api_app.dependency_overrides[get_auth_service] = Service
    response: Response = await api_client.post(
        "/auth/login", data={"username": "admin@example.com", "password": "password1"}
    )
    assert response.status_code == 200 and response.json()["token_type"] == "bearer"


@pytest.mark.api
@pytest.mark.asyncio
async def test_refresh_requires_refresh_token(api_client: AsyncClient) -> None:
    response: Response = await api_client.post("/auth/refresh", json={})
    assert response.status_code == 422
