from sqlalchemy import select

from app.models.complaint_assignment import ComplaintAssignment
from app.models.repair_detail import RepairDetail
from app.repositories.interfaces.repair_repository_interface import (
    RepairRepositoryInterface,
)


class RepairRepository(RepairRepositoryInterface):

    async def get_assignment(self, db, complaint_id: int, lineman_id: int):
        result = await db.execute(
            select(ComplaintAssignment).where(
                ComplaintAssignment.complaint_id == complaint_id,
                ComplaintAssignment.lineman_id == lineman_id
            )
        )

        return result.scalar_one_or_none()

    async def get_repair_by_complaint_id(self, db, complaint_id: int):
        result = await db.execute(
            select(RepairDetail).where(
                RepairDetail.complaint_id == complaint_id
            )
        )

        return result.scalar_one_or_none()

    async def create_repair(self, db, repair_data: dict):
        repair = RepairDetail(**repair_data)

        db.add(repair)
        await db.flush()

        return repair

    async def update_repair_image(self, db, repair, image_path: str):
        repair.repair_image_path = image_path

        await db.commit()
        await db.refresh(repair)

        return repair