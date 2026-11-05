import pytest
from types import SimpleNamespace
from fastapi import FastAPI
from httpx import AsyncClient, Response

from app.api.dependencies.auth_dependency import required_admin
from app.api.dependencies.customer_dependency import get_customer_service
from app.schemas.customer_schema import CustomerCreate


@pytest.mark.api
@pytest.mark.asyncio
async def test_customer_registration_validates_and_creates(
    api_app: FastAPI, api_client: AsyncClient
) -> None:
    class Service:
        async def create_customer(
            self, db: object, payload: CustomerCreate
        ) -> dict[str, object]:
            return {
                "customer_code": "CUS12345678",
                "username": payload.username,
                "email": payload.email,
                "id": 1,
                "phone_number": payload.phone_number,
                "door_no": payload.door_no,
                "street": payload.street,
                "district": payload.district,
                "pincode": payload.pincode,
                "is_active": True,
                "created_at": "2026-01-01T00:00:00Z",
            }

    api_app.dependency_overrides[get_customer_service] = Service
    response: Response = await api_client.post(
        "/customers/",
        json={
            "username": "customer1",
            "email": "c@example.com",
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
async def test_customer_registration_rejects_invalid_payload(
    api_client: AsyncClient,
) -> None:
    response: Response = await api_client.post(
        "/customers/", json={"username": "x", "email": "bad", "password": "short"}
    )
    assert response.status_code == 422


@pytest.mark.api
@pytest.mark.asyncio
async def test_admin_can_list_customers(
    api_app: FastAPI, api_client: AsyncClient, sample_admin: SimpleNamespace
) -> None:
    class Service:
        async def get_all_customers(
            self, db: object, limit: int, offset: int
        ) -> list[object]:
            return []

    api_app.dependency_overrides[required_admin] = lambda: sample_admin
    api_app.dependency_overrides[get_customer_service] = Service
    response: Response = await api_client.get("/customers/")
    assert response.status_code == 200 and response.json() == []


@pytest.mark.api
@pytest.mark.asyncio
async def test_admin_can_get_customer_by_id(
    api_app: FastAPI, api_client: AsyncClient, sample_admin: SimpleNamespace
) -> None:
    class Service:
        async def get_customer_by_id(
            self, db: object, customer_id: int
        ) -> SimpleNamespace:
            return SimpleNamespace(
                id=customer_id,
                customer_code="CUS12345678",
                username="customer1",
                email="customer@example.com",
                phone_number="9876543210",
                door_no="1",
                street="Main",
                district="Test",
                pincode="600001",
                is_active=True,
                created_at="2026-01-01T00:00:00Z",
            )

    api_app.dependency_overrides[required_admin] = lambda: sample_admin
    api_app.dependency_overrides[get_customer_service] = Service
    response: Response = await api_client.get("/customers/3")
    assert response.status_code == 200 and response.json()["id"] == 3


@pytest.mark.api
@pytest.mark.asyncio
async def test_admin_can_deactivate_customer(
    api_app: FastAPI, api_client: AsyncClient, sample_admin: SimpleNamespace
) -> None:
    class Service:
        async def deactivate_customer(
            self, db: object, customer_id: int
        ) -> dict[str, int | bool]:
            return {"id": customer_id, "is_active": False}

    api_app.dependency_overrides[required_admin] = lambda: sample_admin
    api_app.dependency_overrides[get_customer_service] = Service
    response: Response = await api_client.delete("/customers/3")
    assert response.status_code == 200 and response.json()["is_active"] is False
