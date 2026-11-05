from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth_dependency import required_admin
from app.api.dependencies.complaint_report_dependency import (
    get_complaint_report_service,
)
from app.database.database import get_db
from app.models.employee import Employee
from app.schemas.complaint_report_schema import ComplaintStatisticsResponse
from app.services.implementations.complaint_report_service import (
    ComplaintReportService,
)

complaint_report_router: APIRouter = APIRouter(
    prefix="/reports/complaints", tags=["Complaint Reports"]
)


@complaint_report_router.get("/statistics", response_model=ComplaintStatisticsResponse)
async def get_complaint_statistics(
    db: Annotated[AsyncSession, Depends(get_db)],
    report_service: Annotated[
        ComplaintReportService, Depends(get_complaint_report_service)
    ],
    current_admin: Annotated[Employee, Depends(required_admin)],
) -> ComplaintStatisticsResponse:
    return await report_service.get_complaint_statistics(db)
