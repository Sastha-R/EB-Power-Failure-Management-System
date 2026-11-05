import pytest

from app.api.dependencies.auth_dependency import required_admin
from app.api.dependencies.employee_dependency import get_employee_service


@pytest.mark.api
@pytest.mark.asyncio
async def test_employee_list_uses_pagination_and_admin_access(
    api_app, api_client, sample_admin
):
    class Service:
        async def get_all_employees(self, db, limit, offset):
            assert (limit, offset) == (5, 10)
            return []

    api_app.dependency_overrides[required_admin] = lambda: sample_admin
    api_app.dependency_overrides[get_employee_service] = Service
    response = await api_client.get("/employees/?limit=5&offset=10")
    assert response.status_code == 200 and response.json() == []


@pytest.mark.api
@pytest.mark.asyncio
async def test_employee_list_rejects_invalid_pagination(
    api_app, api_client, sample_admin
):
    api_app.dependency_overrides[required_admin] = lambda: sample_admin
    response = await api_client.get("/employees/?limit=0")
    assert response.status_code == 422
