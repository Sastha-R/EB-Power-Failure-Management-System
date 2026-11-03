from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.complaint import Complaint
from app.repositories.interfaces.complaint_repository_interface import (
    ComplaintRepositoryInterface,
)


class ComplaintRepository(ComplaintRepositoryInterface):

    async def create_complaint(
        self,
        db: AsyncSession,
        complaint_data: dict
    ):
        complaint = Complaint(**complaint_data)

        db.add(complaint)

        await db.commit()
        await db.refresh(complaint)

        return complaint

    async def get_customer_complaints(
        self,
        db: AsyncSession,
        customer_id: int
    ):
        result = await db.execute(
            select(Complaint).where(
                Complaint.customer_id == customer_id
            )
        )

        return result.scalars().all()