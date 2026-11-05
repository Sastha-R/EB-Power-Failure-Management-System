import pytest
from types import SimpleNamespace
from fastapi import FastAPI
from httpx import AsyncClient, Response

from app.api.dependencies.auth_dependency import required_admin
from app.api.dependencies.employee_dependency import get_employee_service
from app.schemas.employee_schema import EmployeeCreate


@pytest.mark.api
@pytest.mark.asyncio
async def test_employee_list_uses_pagination_and_admin_access(
    api_app: FastAPI, api_client: AsyncClient, sample_admin: SimpleNamespace
) -> None:
    class Service:
        async def get_all_employees(
            self, db: object, limit: int, offset: int
        ):
            assert (limit, offset) == (5, 10)
            return []

    api_app.dependency_overrides[required_admin] = lambda: sample_admin
    api_app.dependency_overrides[get_employee_service] = Service
    response: Response = await api_client.get("/employees/?limit=5&offset=10")
    assert response.status_code == 200 and response.json() == []


@pytest.mark.api
@pytest.mark.asyncio
async def test_employee_list_rejects_invalid_pagination(
    api_app: FastAPI, api_client: AsyncClient, sample_admin: SimpleNamespace
) -> None:
    api_app.dependency_overrides[required_admin] = lambda: sample_admin
    response: Response = await api_client.get("/employees/?limit=0")
    assert response.status_code == 422


@pytest.mark.api
@pytest.mark.asyncio
async def test_admin_can_create_employee(
    api_app: FastAPI, api_client: AsyncClient, sample_admin: SimpleNamespace
) -> None:
    class Service:
        async def create_employee(
            self, db: object, payload: EmployeeCreate
        ) -> SimpleNamespace:
            return SimpleNamespace(
                id=4,
                employee_code="EMP12345678",
                username=payload.username,
                email=payload.email,
                role="lineman",
                phone_number=payload.phone_number,
                door_no=payload.door_no,
                street=payload.street,
                district=payload.district,
                pincode=payload.pincode,
                is_active=True,
                created_at="2026-01-01T00:00:00Z",
            )

    api_app.dependency_overrides[required_admin] = lambda: sample_admin
    api_app.dependency_overrides[get_employee_service] = Service
    response: Response = await api_client.post(
        "/employees/",
        json={
            "username": "lineman1",
            "email": "lineman@example.com",
            "password": "password1",
            "phone_number": "9876543210",
            "door_no": "1",
            "street": "Main",
            "district": "Test",
            "pincode": "600001",
        },
    )
    assert response.status_code == 201


@pytest.mark.api
@pytest.mark.asyncio
async def test_admin_can_get_employee_by_id(
    api_app: FastAPI, api_client: AsyncClient, sample_admin: SimpleNamespace
) -> None:
    class Service:
        async def get_employee_by_id(
            self, db: object, employee_id: int
        ) -> SimpleNamespace:
            return SimpleNamespace(
                id=employee_id,
                employee_code="EMP12345678",
                username="lineman1",
                email="lineman@example.com",
                role="lineman",
                phone_number="9876543210",
                door_no="1",
                street="Main",
                district="Test",
                pincode="600001",
                is_active=True,
                created_at="2026-01-01T00:00:00Z",
            )

    api_app.dependency_overrides[required_admin] = lambda: sample_admin
    api_app.dependency_overrides[get_employee_service] = Service
    response: Response = await api_client.get("/employees/4")
    assert response.status_code == 200 and response.json()["id"] == 4


@pytest.mark.api
@pytest.mark.asyncio
async def test_admin_can_deactivate_employee(
    api_app: FastAPI, api_client: AsyncClient, sample_admin: SimpleNamespace
) -> None:
    class Service:
        async def deactivate_employee(
            self, db: object, employee_id: int
        ) -> dict[str, int | bool]:
            return {"id": employee_id, "is_active": False}

    api_app.dependency_overrides[required_admin] = lambda: sample_admin
    api_app.dependency_overrides[get_employee_service] = Service
    response: Response = await api_client.delete("/employees/4")
    assert response.status_code == 200 and response.json()["is_active"] is False


