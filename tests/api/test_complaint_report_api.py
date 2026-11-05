import pytest
from fastapi import FastAPI
from httpx import AsyncClient, Response
from types import SimpleNamespace

from app.api.dependencies.auth_dependency import get_current_employee, required_admin
from app.api.dependencies.complaint_report_dependency import (
    get_complaint_report_service,
)
from app.core.security import create_access_token


@pytest.mark.api
@pytest.mark.asyncio
async def test_admin_can_get_complaint_statistics(
    api_app: FastAPI, api_client: AsyncClient, sample_admin: SimpleNamespace
) -> None:
    expected: dict[str, int] = {
        "total_complaints": 7,
        "pending": 1,
        "assigned": 2,
        "repair_completed": 1,
        "closed": 3,
    }

    class Service:
        async def get_complaint_statistics(self, db: object) -> dict[str, int]:
            return expected

    api_app.dependency_overrides[required_admin] = lambda: sample_admin
    api_app.dependency_overrides[get_complaint_report_service] = Service
    response: Response = await api_client.get("/reports/complaints/statistics")

    assert response.status_code == 200
    assert response.json() == expected


@pytest.mark.api
@pytest.mark.asyncio
async def test_complaint_statistics_requires_authentication(
    api_client: AsyncClient,
) -> None:
    response: Response = await api_client.get("/reports/complaints/statistics")
    assert response.status_code == 401


@pytest.mark.api
@pytest.mark.asyncio
async def test_lineman_cannot_get_complaint_statistics(
    api_app: FastAPI, api_client: AsyncClient, sample_lineman: SimpleNamespace
) -> None:
    api_app.dependency_overrides[get_current_employee] = lambda: sample_lineman
    response: Response = await api_client.get("/reports/complaints/statistics")
    assert response.status_code == 403


@pytest.mark.api
@pytest.mark.asyncio
async def test_customer_cannot_get_complaint_statistics(
    api_client: AsyncClient,
) -> None:
    token: str = create_access_token(3, "customer")
    response: Response = await api_client.get(
        "/reports/complaints/statistics",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403
