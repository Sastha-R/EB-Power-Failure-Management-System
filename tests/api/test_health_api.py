import pytest
from fastapi import FastAPI
from httpx import AsyncClient, Response

from app.api.dependencies.health_dependency import get_health_service


@pytest.mark.api
@pytest.mark.asyncio
async def test_health_endpoint_returns_service_status(
    api_app: FastAPI, api_client: AsyncClient
) -> None:
    class Service:
        async def check_health(self, db: object) -> dict[str, str]:
            return {
                "status": "healthy",
                "application": "running",
                "database": "connected",
            }

    api_app.dependency_overrides[get_health_service] = Service
    response: Response = await api_client.get("/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
