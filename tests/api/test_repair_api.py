import pytest
from fastapi import FastAPI, UploadFile
from httpx import AsyncClient, Response
from types import SimpleNamespace

from app.api.dependencies.auth_dependency import required_lineman
from app.api.dependencies.repair_dependency import get_repair_service
from app.api.dependencies.auth_dependency import required_admin
from app.schemas.repair_schema import RepairCreate


@pytest.mark.api
@pytest.mark.asyncio
async def test_lineman_can_complete_repair(
    api_app: FastAPI, api_client: AsyncClient, sample_lineman: SimpleNamespace
) -> None:
    class Service:
        async def complete_repair(
            self,
            db: object,
            complaint_id: int,
            lineman_id: int,
            data: RepairCreate,
        ) -> dict[str, object]:
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
    response: Response = await api_client.post(
        "/repairs/5/complete",
        json={"issue_found": "Cable fault", "repair_description": "Cable replaced"},
    )
    assert response.status_code == 201


@pytest.mark.api
@pytest.mark.asyncio
async def test_repair_completion_requires_authentication(
    api_client: AsyncClient,
) -> None:
    response: Response = await api_client.post(
        "/repairs/5/complete",
        json={"issue_found": "Cable fault", "repair_description": "Cable replaced"},
    )
    assert response.status_code == 401


@pytest.mark.api
@pytest.mark.asyncio
async def test_admin_can_list_repair_details(
    api_app: FastAPI, api_client: AsyncClient, sample_admin: SimpleNamespace
) -> None:
    class Service:
        async def get_all_repair_details(self, db: object) -> list[object]:
            return []

    api_app.dependency_overrides[required_admin] = lambda: sample_admin
    api_app.dependency_overrides[get_repair_service] = Service
    response: Response = await api_client.get("/repairs/")
    assert response.status_code == 200 and response.json() == []


@pytest.mark.api
@pytest.mark.asyncio
async def test_lineman_can_upload_repair_image(
    api_app: FastAPI, api_client: AsyncClient, sample_lineman: SimpleNamespace
) -> None:
    class Service:
        async def upload_repair_image(
            self,
            db: object,
            complaint_id: int,
            lineman_id: int,
            image: UploadFile,
        ) -> dict[str, str]:
            assert complaint_id == 5
            assert lineman_id == sample_lineman.id
            assert image.filename == "repair.png"
            return {"message": "Repair image uploaded"}

    api_app.dependency_overrides[required_lineman] = lambda: sample_lineman
    api_app.dependency_overrides[get_repair_service] = Service
    response: Response = await api_client.post(
        "/repairs/5/image",
        files={"image": ("repair.png", b"test image", "image/png")},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Repair image uploaded"
