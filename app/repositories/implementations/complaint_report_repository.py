from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.complaint import Complaint
from app.repositories.interfaces.complaint_report_repository_interface import (
    ComplaintReportRepositoryInterface,
)


class ComplaintReportRepository(ComplaintReportRepositoryInterface):
    async def get_complaint_statistics(self, db: AsyncSession) -> dict[str, int]:
        statuses = ("PENDING", "ASSIGNED", "REPAIR_COMPLETED", "CLOSED")
        counts = [
            func.coalesce(
                func.sum(case((Complaint.status == status, 1), else_=0)), 0
            ).label(status.lower())
            for status in statuses
        ]
        statement = select(func.count(Complaint.id).label("total_complaints"), *counts)
        result = await db.execute(statement)
        row = result.one()

        return {
            "total_complaints": int(row.total_complaints),
            "pending": int(row.pending),
            "assigned": int(row.assigned),
            "repair_completed": int(row.repair_completed),
            "closed": int(row.closed),
        }
