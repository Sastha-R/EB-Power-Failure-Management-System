import pytest

from app.api.dependencies.health_dependency import get_health_service


@pytest.mark.api
@pytest.mark.asyncio
async def test_health_endpoint_returns_service_status(api_app, api_client):
    class Service:
        async def check_health(self, db):
            return {
                "status": "healthy",
                "application": "running",
                "database": "connected",
            }

    api_app.dependency_overrides[get_health_service] = Service
    response = await api_client.get("/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
