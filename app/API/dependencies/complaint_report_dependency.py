from app.repositories.implementations.complaint_report_repository import (
    ComplaintReportRepository,
)
from app.services.implementations.complaint_report_service import (
    ComplaintReportService,
)


def get_complaint_report_service() -> ComplaintReportService:
    complaint_report_repository: ComplaintReportRepository = ComplaintReportRepository()
    return ComplaintReportService(complaint_report_repository)
