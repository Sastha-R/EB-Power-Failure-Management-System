from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth_dependency import required_lineman
from app.api.dependencies.repair_dependency import get_repair_service
from app.database.database import get_db
from app.models.employee import Employee
from app.schemas.repair_schema import RepairCreate, RepairResponse
from app.services.implementations.repair_service import RepairService

from fastapi import File, UploadFile
from app.utils.file_upload import upload_image
from app.core.config import settings

repair_router = APIRouter(prefix="/repairs", tags=["Repairs"])


@repair_router.post(
    "/{complaint_id}/complete",
    response_model=RepairResponse,
    status_code=status.HTTP_201_CREATED,
)
async def complete_repair(
    complaint_id: int,
    repair_data: RepairCreate,
    current_lineman: Annotated[Employee, Depends(required_lineman)],
    db: Annotated[AsyncSession, Depends(get_db)],
    repair_service: Annotated[RepairService, Depends(get_repair_service)],
):
    return await repair_service.complete_repair(
        db, complaint_id, current_lineman.id, repair_data
    )


@repair_router.post("/{complaint_id}/image")
async def upload_repair_image(
    complaint_id: int,
    image: Annotated[UploadFile, File()],
    current_lineman: Annotated[Employee, Depends(required_lineman)],
    db: Annotated[AsyncSession, Depends(get_db)],
    repair_service: Annotated[RepairService, Depends(get_repair_service)],
):
    return await repair_service.upload_repair_image(
        db,
        complaint_id,
        current_lineman.id,
        image,
    )