from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.complaint import Complaint
from app.models.complaint_assignment import ComplaintAssignment
from app.repositories.interfaces.complaint_repository_interface import (
    ComplaintRepositoryInterface,
)


class ComplaintRepository(ComplaintRepositoryInterface):
    async def create_complaint(self, db: AsyncSession, complaint_data: dict):
        complaint = Complaint(**complaint_data)

        db.add(complaint)

        await db.commit()
        await db.refresh(complaint)

        return complaint

    async def get_customer_complaints(self, db: AsyncSession, customer_id: int):
        result = await db.execute(
            select(Complaint).where(Complaint.customer_id == customer_id)
        )

        return result.scalars().all()

    async def get_all_complaints(self, db: AsyncSession):

        result = await db.execute(select(Complaint))

        return result.scalars().all()

    async def assign_complaint(self, db: AsyncSession, assignment_data: dict):
        assignment = ComplaintAssignment(**assignment_data)

        db.add(assignment)

        await db.commit()
        await db.refresh(assignment)

        return assignment

    async def get_complaint_by_id(self, db: AsyncSession, complaint_id: int):
        result = await db.execute(select(Complaint).where(Complaint.id == complaint_id))

        return result.scalar_one_or_none()

    async def get_assigned_complaints(self, db: AsyncSession, lineman_id: int):
        result = await db.execute(
            select(Complaint)
            .join(ComplaintAssignment, Complaint.id == ComplaintAssignment.complaint_id)
            .where(ComplaintAssignment.lineman_id == lineman_id)
        )

        return result.scalars().all()

    async def close_complaint(self, db, complaint):

        complaint.status = "CLOSED"

        await db.commit()
        await db.refresh(complaint)

        return complaint

    async def update_complaint_image(self, db, complaint, image_path: str):

        complaint.image_path = image_path

        await db.commit()
        await db.refresh(complaint)

        return complaint

    async def update_complaint(
        self,
        db: AsyncSession,
        complaint,
        complaint_data: dict,
    ):
        for key, value in complaint_data.items():
            setattr(complaint, key, value)

        await db.commit()
        await db.refresh(complaint)

        return complaint