from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.implementations.complaint_report_repository import (
    ComplaintReportRepository,
)
from app.services.interfaces.complaint_report_service_interface import (
    ComplaintReportServiceInterface,
)


class ComplaintReportService(ComplaintReportServiceInterface):
    def __init__(self, complaint_report_repository: ComplaintReportRepository):
        self.complaint_report_repository = complaint_report_repository

    async def get_complaint_statistics(self, db: AsyncSession) -> dict[str, int]:
        return await self.complaint_report_repository.get_complaint_statistics(db)
