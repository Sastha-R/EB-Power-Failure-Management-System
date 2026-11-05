import pytest

from app.api.dependencies.customer_dependency import get_customer_service


@pytest.mark.api
@pytest.mark.asyncio
async def test_customer_registration_validates_and_creates(api_app, api_client):
    class Service:
        async def create_customer(self, db, payload):
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
    response = await api_client.post(
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
async def test_customer_registration_rejects_invalid_payload(api_client):
    response = await api_client.post(
        "/customers/", json={"username": "x", "email": "bad", "password": "short"}
    )
    assert response.status_code == 422
