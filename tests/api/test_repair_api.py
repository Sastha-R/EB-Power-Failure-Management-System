import pytest

from app.api.dependencies.auth_dependency import required_lineman
from app.api.dependencies.repair_dependency import get_repair_service


@pytest.mark.api
@pytest.mark.asyncio
async def test_lineman_can_complete_repair(api_app, api_client, sample_lineman):
    class Service:
        async def complete_repair(self, db, complaint_id, lineman_id, data):
            return {
                "id": 1,
                "complaint_id": complaint_id,
                "lineman_id": lineman_id,
                "issue_found": data.issue_found,
                "repair_description": data.repair_description,
                "repair_completed_at": "2026-01-01T00:00:00Z",
                "repair_image_path": None,
                "remarks": None,
            }

    api_app.dependency_overrides[required_lineman] = lambda: sample_lineman
    api_app.dependency_overrides[get_repair_service] = Service
    response = await api_client.post(
        "/repairs/5/complete",
        json={"issue_found": "Cable fault", "repair_description": "Cable replaced"},
    )
    assert response.status_code == 201


@pytest.mark.api
@pytest.mark.asyncio
async def test_repair_completion_requires_authentication(api_client):
    response = await api_client.post(
        "/repairs/5/complete",
        json={"issue_found": "Cable fault", "repair_description": "Cable replaced"},
    )
    assert response.status_code == 401
