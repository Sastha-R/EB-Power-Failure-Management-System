from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth_dependency import get_current_customer
from app.api.dependencies.complaint_dependency import get_complaint_service
from app.database.database import get_db
from app.models.customer import Customer
from app.schemas.complaint_schema import ComplaintCreate
from app.services.implementations.complaint_service import ComplaintService

complaint_router = APIRouter(
    prefix="/complaints",
    tags=["Complaints"]
)


@complaint_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_complaint(
    complaint_data: ComplaintCreate,
    current_customer: Annotated[
        Customer, Depends(get_current_customer)
    ],
    db: Annotated[AsyncSession, Depends(get_db)],
    complaint_service: Annotated[
        ComplaintService, Depends(get_complaint_service)
    ]
):
    return await complaint_service.create_complaint(
        db,
        current_customer.id,
        complaint_data
    )

@complaint_router.get("/my")
async def get_my_complaints(
    current_customer: Annotated[
        Customer, Depends(get_current_customer)
    ],
    db: Annotated[AsyncSession, Depends(get_db)],
    complaint_service: Annotated[
        ComplaintService, Depends(get_complaint_service)
    ]
):
    return await complaint_service.get_customer_complaints(
        db,
        current_customer.id
    )