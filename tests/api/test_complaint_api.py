import pytest

from app.api.dependencies.auth_dependency import (
    get_current_customer,
    required_admin,
    required_lineman,
)
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


@pytest.mark.api
@pytest.mark.asyncio
async def test_customer_can_list_their_complaints(
    api_app, api_client, sample_customer
):
    class Service:
        async def get_customer_complaints(self, db, customer_id):
            assert customer_id == sample_customer.id
            return []

    api_app.dependency_overrides[get_current_customer] = lambda: sample_customer
    api_app.dependency_overrides[get_complaint_service] = Service
    response = await api_client.get("/complaints/my")
    assert response.status_code == 200 and response.json() == []


@pytest.mark.api
@pytest.mark.asyncio
async def test_admin_can_list_all_complaints(api_app, api_client, sample_admin):
    class Service:
        async def get_all_complaints(self, db):
            return []

    api_app.dependency_overrides[required_admin] = lambda: sample_admin
    api_app.dependency_overrides[get_complaint_service] = Service
    response = await api_client.get("/complaints/")
    assert response.status_code == 200 and response.json() == []


@pytest.mark.api
@pytest.mark.asyncio
async def test_lineman_can_list_assigned_complaints(
    api_app, api_client, sample_lineman
):
    class Service:
        async def get_assigned_complaints(self, db, lineman_id):
            assert lineman_id == sample_lineman.id
            return []

    api_app.dependency_overrides[required_lineman] = lambda: sample_lineman
    api_app.dependency_overrides[get_complaint_service] = Service
    response = await api_client.get("/complaints/assigned")
    assert response.status_code == 200 and response.json() == []


@pytest.mark.api
@pytest.mark.asyncio
async def test_admin_can_close_complaint(api_app, api_client, sample_admin):
    class Service:
        async def close_complaint(self, db, complaint_id):
            return {"id": complaint_id, "status": "CLOSED"}

    api_app.dependency_overrides[required_admin] = lambda: sample_admin
    api_app.dependency_overrides[get_complaint_service] = Service
    response = await api_client.patch("/complaints/12/close")
    assert response.status_code == 200 and response.json()["status"] == "CLOSED"


@pytest.mark.api
@pytest.mark.asyncio
async def test_customer_can_update_pending_complaint(
    api_app, api_client, sample_customer
):
    class Service:
        async def update_complaint(self, db, complaint_id, customer_id, data):
            return {
                "id": complaint_id,
                "complaint_number": "CMP12345678",
                "customer_id": customer_id,
                "door_no": "1",
                "street": "Main",
                "district": "Test",
                "pincode": "600001",
                "failure_type": "Outage",
                "description": data.description,
                "priority": "NORMAL",
                "status": "PENDING",
                "image_path": None,
                "created_at": "2026-01-01T00:00:00Z",
                "updated_at": "2026-01-01T00:00:00Z",
            }

    api_app.dependency_overrides[get_current_customer] = lambda: sample_customer
    api_app.dependency_overrides[get_complaint_service] = Service
    response = await api_client.patch(
        "/complaints/12", json={"description": "Power issue continues"}
    )
    assert response.status_code == 200
    assert response.json()["description"] == "Power issue continues"
