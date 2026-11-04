from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.exceptions.custom_exceptions.complaint_exceptions import ComplaintNotFoundError
from app.exceptions.custom_exceptions.repair_exceptions import (
    RepairAlreadyCompletedError,
    RepairNotAllowedError,
    RepairNotAssignedError,
    RepairNotFoundError,
)
from app.repositories.implementations.complaint_repository import ComplaintRepository
from app.repositories.implementations.repair_repository import RepairRepository
from app.services.interfaces.repair_service_interface import RepairServiceInterface
from app.utils.file_upload import upload_image


class RepairService(RepairServiceInterface):
    def __init__(
        self,
        repair_repository: RepairRepository,
        complaint_repository: ComplaintRepository,
    ):
        self.repair_repository = repair_repository
        self.complaint_repository = complaint_repository

    async def complete_repair(
        self, db, complaint_id: int, lineman_id: int, repair_data
    ):
        # Check whether complaint exists
        complaint = await self.complaint_repository.get_complaint_by_id(
            db, complaint_id
        )

        if not complaint:
            raise ComplaintNotFoundError()

        # Check whether complaint is assigned to this lineman
        assignment = await self.repair_repository.get_assignment(
            db, complaint_id, lineman_id
        )

        if not assignment:
            raise RepairNotAssignedError()

        # Check complaint status
        if complaint.status != "ASSIGNED":
            raise RepairNotAllowedError(
                "Complaint is not available for repair completion"
            )

        # Prevent duplicate repair submission
        existing_repair = await self.repair_repository.get_repair_by_complaint_id(
            db, complaint_id
        )

        if existing_repair:
            raise RepairAlreadyCompletedError()

        # Prepare repair data
        repair_dict = repair_data.model_dump()
        repair_dict["complaint_id"] = complaint_id
        repair_dict["lineman_id"] = lineman_id

        try:
            # Save repair details
            repair = await self.repair_repository.create_repair(db, repair_dict)

            # Update complaint status
            complaint.status = "REPAIR_COMPLETED"

            await db.commit()
            await db.refresh(repair)

            return repair

        except Exception:
            await db.rollback()
            raise

    async def upload_repair_image(
        self, db, complaint_id: int, lineman_id: int, image: UploadFile
    ):
        complaint = await self.complaint_repository.get_complaint_by_id(
            db, complaint_id
        )

        if not complaint:
            raise ComplaintNotFoundError()

        assignment = await self.repair_repository.get_assignment(
            db, complaint_id, lineman_id
        )

        if not assignment:
            raise RepairNotAssignedError()

        if complaint.status != "REPAIR_COMPLETED":
            raise RepairNotAllowedError(
                "Repair image can only be uploaded after repair completion"
            )

        repair = await self.repair_repository.get_repair_by_complaint_id(
            db, complaint_id
        )

        if not repair:
            raise RepairNotFoundError("Repair details not found")

        image_path = await upload_image(
            image,
            settings.REPAIR_UPLOAD_DIR,
        )

        return await self.repair_repository.update_repair_image(db, repair, image_path)

    async def get_all_repair_details(self, db: AsyncSession):
        return await self.repair_repository.get_all_repair_details(db)
