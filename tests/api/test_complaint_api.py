import pytest

from app.api.dependencies.auth_dependency import get_current_customer
from app.api.dependencies.complaint_dependency import get_complaint_service


@pytest.mark.api
@pytest.mark.asyncio
async def test_customer_can_create_complaint(api_app, api_client, sample_customer):
    class Service:
        async def create_complaint(self, db, customer_id, data):
            return {
                "id": 1,
                "customer_id": customer_id,
                "complaint_number": "CMP12345678",
                **data.model_dump(),
                "priority": "NORMAL",
                "status": "PENDING",
                "image_path": None,
                "created_at": "2026-01-01T00:00:00Z",
                "updated_at": "2026-01-01T00:00:00Z",
            }

    api_app.dependency_overrides[get_current_customer] = lambda: sample_customer
    api_app.dependency_overrides[get_complaint_service] = Service
    response = await api_client.post(
        "/complaints/",
        json={
            "door_no": "1",
            "street": "Main",
            "district": "Test",
            "pincode": "600001",
            "failure_type": "Outage",
            "description": "Power has been unavailable",
        },
    )
    assert response.status_code == 201


@pytest.mark.api
@pytest.mark.asyncio
async def test_complaint_assignment_requires_admin(api_client):
    response = await api_client.post(
        "/complaints/assign", json={"complaint_id": 1, "lineman_id": 2}
    )
    assert response.status_code == 401
