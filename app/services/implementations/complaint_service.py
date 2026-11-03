import uuid

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.repositories.implementations.complaint_repository import (
    ComplaintRepository,
)
from app.repositories.implementations.employee_repository import EmployeeRepository
from app.services.interfaces.complaint_service_interface import (
    ComplaintServiceInterface,
)
from app.utils.file_upload import upload_image


class ComplaintService(ComplaintServiceInterface):
    def __init__(
        self,
        complaint_repository: ComplaintRepository,
        employee_repository: EmployeeRepository,
    ):
        self.complaint_repository = complaint_repository
        self.employee_repository = employee_repository

    async def create_complaint(
        self, db: AsyncSession, customer_id: int, complaint_data
    ):
        complaint_dict = complaint_data.model_dump()

        complaint_dict["customer_id"] = customer_id

        complaint_dict["complaint_number"] = f"CMP{uuid.uuid4().hex[:8].upper()}"

        complaint_dict["door_no"] = complaint_dict.get("door_no")
        complaint_dict["street"] = complaint_dict.get("street")
        complaint_dict["district"] = complaint_dict.get("district")
        complaint_dict["pincode"] = complaint_dict.get("pincode")

        return await self.complaint_repository.create_complaint(db, complaint_dict)

    async def get_customer_complaints(self, db: AsyncSession, customer_id: int):
        return await self.complaint_repository.get_customer_complaints(db, customer_id)

    async def get_all_complaints(self, db: AsyncSession):
        return await self.complaint_repository.get_all_complaints(db)

    async def assign_complaint(self, db: AsyncSession, admin_id: int, assignment_data):
        # Check whether the complaint exists
        complaint = await self.complaint_repository.get_complaint_by_id(
            db, assignment_data.complaint_id
        )

        if not complaint:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found"
            )

        # Check complaint status
        if complaint.status != "PENDING":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Complaint is not available for assignment",
            )

        # Check whether the employee exists
        lineman = await self.employee_repository.get_employee_by_id(
            db, assignment_data.lineman_id
        )

        if not lineman or lineman.role != "lineman":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Lineman not found"
            )

        if not lineman.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Lineman account is inactive",
            )

        # Prepare assignment data
        assignment_dict = assignment_data.model_dump()
        assignment_dict["assigned_by"] = admin_id

        # Update complaint status
        complaint.status = "ASSIGNED"

        return await self.complaint_repository.assign_complaint(db, assignment_dict)

    async def get_assigned_complaints(self, db: AsyncSession, lineman_id: int):
        return await self.complaint_repository.get_assigned_complaints(db, lineman_id)

    async def close_complaint(self, db, complaint_id: int):
        complaint = await self.complaint_repository.get_complaint_by_id(
            db, complaint_id
        )

        if not complaint:
            raise HTTPException(status_code=404, detail="Complaint not found")

        if complaint.status != "REPAIR_COMPLETED":
            raise HTTPException(
                status_code=400,
                detail="Complaint cannot be closed before repair completion",
            )

        return await self.complaint_repository.close_complaint(db, complaint)

    async def upload_complaint_image(
        self, db, complaint_id: int, customer_id: int, image: UploadFile
    ):
        complaint = await self.complaint_repository.get_complaint_by_id(
            db, complaint_id
        )

        if not complaint:
            raise HTTPException(status_code=404, detail="Complaint not found")

        if complaint.customer_id != customer_id:
            raise HTTPException(
                status_code=403,
                detail="You cannot upload an image for another customer's complaint",
            )

        if complaint.status != "PENDING":
            raise HTTPException(
                status_code=400,
                detail="Image can only be uploaded while the complaint is pending",
            )

        image_path = await upload_image(
            image,
            settings.COMPLAINT_UPLOAD_DIR,
        )

        return await self.complaint_repository.update_complaint_image(
            db, complaint, image_path
        )
