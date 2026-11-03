import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.implementations.complaint_repository import (
    ComplaintRepository,
)
from app.services.interfaces.complaint_service_interface import (
    ComplaintServiceInterface,
)


class ComplaintService(ComplaintServiceInterface):
    def __init__(self, complaint_repository: ComplaintRepository):
        self.complaint_repository = complaint_repository

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


    async def get_customer_complaints(
        self,
        db: AsyncSession,
        customer_id: int
    ):
        return await self.complaint_repository.get_customer_complaints(
            db,
            customer_id
        )