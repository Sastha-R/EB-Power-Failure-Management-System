from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth_dependency import (
    get_current_customer,
    required_admin,
    required_lineman,
)
from app.api.dependencies.complaint_dependency import get_complaint_service
from app.database.database import get_db
from app.models.customer import Customer
from app.models.employee import Employee
from app.schemas.assignment_schema import AssignmentCreate
from app.schemas.complaint_schema import ComplaintCreate
from app.services.implementations.complaint_service import ComplaintService

complaint_router = APIRouter(prefix="/complaints", tags=["Complaints"])


@complaint_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_complaint(
    complaint_data: ComplaintCreate,
    current_customer: Annotated[Customer, Depends(get_current_customer)],
    db: Annotated[AsyncSession, Depends(get_db)],
    complaint_service: Annotated[ComplaintService, Depends(get_complaint_service)],
):
    return await complaint_service.create_complaint(
        db, current_customer.id, complaint_data
    )


@complaint_router.get("/my")
async def get_my_complaints(
    current_customer: Annotated[Customer, Depends(get_current_customer)],
    db: Annotated[AsyncSession, Depends(get_db)],
    complaint_service: Annotated[ComplaintService, Depends(get_complaint_service)],
):
    return await complaint_service.get_customer_complaints(db, current_customer.id)


@complaint_router.get("/")
async def get_all_complaints(
    current_admin: Annotated[Employee, Depends(required_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
    complaint_service: Annotated[ComplaintService, Depends(get_complaint_service)],
):
    return await complaint_service.get_all_complaints(db)


@complaint_router.post("/assign")
async def assign_complaint(
    assignment_data: AssignmentCreate,
    current_admin: Annotated[Employee, Depends(required_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
    complaint_service: Annotated[ComplaintService, Depends(get_complaint_service)],
):
    return await complaint_service.assign_complaint(
        db, current_admin.id, assignment_data
    )


@complaint_router.get("/assigned")
async def get_assigned_complaints(
    current_employee: Annotated[Employee, Depends(required_lineman)],
    db: Annotated[AsyncSession, Depends(get_db)],
    complaint_service: Annotated[ComplaintService, Depends(get_complaint_service)],
):
    return await complaint_service.get_assigned_complaints(db, current_employee.id)


@complaint_router.patch("/{complaint_id}/close")
async def close_complaint(
    complaint_id: int,
    current_admin: Annotated[Employee, Depends(required_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
    complaint_service: Annotated[ComplaintService, Depends(get_complaint_service)],
):
    return await complaint_service.close_complaint(db, complaint_id)


@complaint_router.post("/{complaint_id}/image")
async def upload_complaint_image(
    complaint_id: int,
    image: Annotated[UploadFile, File()],
    current_customer: Annotated[Customer, Depends(get_current_customer)],
    db: Annotated[AsyncSession, Depends(get_db)],
    complaint_service: Annotated[ComplaintService, Depends(get_complaint_service)],
):
    return await complaint_service.upload_complaint_image(
        db,
        complaint_id,
        current_customer.id,
        image,
    )
