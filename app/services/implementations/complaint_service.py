import logging
import uuid

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.concurrency import run_in_threadpool

from app.core.config import settings
from app.exceptions.custom_exceptions.complaint_exceptions import (
    ComplaintNotEditableError,
    ComplaintNotFoundError,
    ComplaintNotReadyToCloseError,
    UnauthorizedComplaintAccessError,
)
from app.exceptions.custom_exceptions.employee_exceptions import (
    EmployeeAlreadyInactiveError,
    EmployeeNotFoundError,
)
from app.models.complaint import Complaint
from app.models.complaint_assignment import ComplaintAssignment
from app.models.customer import Customer
from app.models.employee import Employee
from app.repositories.implementations.complaint_repository import (
    ComplaintRepository,
)
from app.repositories.implementations.customer_repository import CustomerRepository
from app.repositories.implementations.employee_repository import EmployeeRepository
from app.schemas.assignment_schema import AssignmentCreate
from app.schemas.complaint_schema import ComplaintCreate, ComplaintUpdate
from app.services.interfaces.complaint_service_interface import (
    ComplaintServiceInterface,
)
from app.utils.email import send_complaint_closed_email, send_complaint_registered_email
from app.utils.file_upload import upload_image

logger: logging.Logger = logging.getLogger(__name__)


class ComplaintService(ComplaintServiceInterface):
    def __init__(
        self,
        complaint_repository: ComplaintRepository,
        employee_repository: EmployeeRepository,
        customer_repository: CustomerRepository,
    ) -> None:
        self.complaint_repository = complaint_repository
        self.employee_repository = employee_repository
        self.customer_repository = customer_repository

    async def create_complaint(
        self, db: AsyncSession, customer_id: int, complaint_data: ComplaintCreate
    ) -> Complaint:
        complaint_dict = complaint_data.model_dump()

        complaint_dict["customer_id"] = customer_id
        complaint_dict["complaint_number"] = f"CMP{uuid.uuid4().hex[:8].upper()}"

        complaint: Complaint = await self.complaint_repository.create_complaint(
            db, complaint_dict
        )

        customer = await self.customer_repository.get_customer_by_id(db, customer_id)

        await run_in_threadpool(
            send_complaint_registered_email,
            customer.email,
            complaint.complaint_number,
        )
        logger.info(f"Complaint {complaint.complaint_number} created successfully")
        return complaint

    async def get_customer_complaints(
        self, db: AsyncSession, customer_id: int
    ) -> list[Complaint]:
        return await self.complaint_repository.get_customer_complaints(db, customer_id)

    async def get_all_complaints(self, db: AsyncSession) -> list[Complaint]:
        return await self.complaint_repository.get_all_complaints(db)

    async def assign_complaint(
        self, db: AsyncSession, admin_id: int, assignment_data: AssignmentCreate
    ) -> ComplaintAssignment:
        complaint: (
            Complaint | None
        ) = await self.complaint_repository.get_complaint_by_id(
            db, assignment_data.complaint_id
        )

        if not complaint:
            raise ComplaintNotFoundError()

        if complaint.status != "PENDING":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Complaint is not available for assignment",
            )

        lineman: Employee | None = await self.employee_repository.get_employee_by_id(
            db, assignment_data.lineman_id
        )

        if not lineman or lineman.role != "lineman":
            raise EmployeeNotFoundError("Lineman not found")

        if not lineman.is_active:
            raise EmployeeAlreadyInactiveError("Lineman account is inactive")

        assignment_dict = assignment_data.model_dump()
        assignment_dict["assigned_by"] = admin_id

        # Update complaint status
        complaint.status = "ASSIGNED"
        logger.info(
            "Complaint %s assigned to lineman ID %s by admin ID %s",
            complaint.complaint_number,
            assignment_data.lineman_id,
            admin_id,
        )
        return await self.complaint_repository.assign_complaint(db, assignment_dict)

    async def get_assigned_complaints(
        self, db: AsyncSession, lineman_id: int
    ) -> list[Complaint]:
        return await self.complaint_repository.get_assigned_complaints(db, lineman_id)

    async def close_complaint(self, db: AsyncSession, complaint_id: int) -> Complaint:
        complaint: (
            Complaint | None
        ) = await self.complaint_repository.get_complaint_by_id(db, complaint_id)

        if not complaint:
            raise ComplaintNotFoundError()

        if complaint.status != "REPAIR_COMPLETED":
            raise ComplaintNotReadyToCloseError(
                "Complaint cannot be closed before repair completion"
            )

        closed_complaint: Complaint = await self.complaint_repository.close_complaint(
            db, complaint
        )

        customer: Customer | None = await self.customer_repository.get_customer_by_id(
            db, closed_complaint.customer_id
        )

        await run_in_threadpool(
            send_complaint_closed_email,
            customer.email,
            closed_complaint.complaint_number,
        )

        return closed_complaint

    async def upload_complaint_image(
        self,
        db: AsyncSession,
        complaint_id: int,
        customer_id: int,
        image: UploadFile,
    ) -> Complaint:
        complaint: (
            Complaint | None
        ) = await self.complaint_repository.get_complaint_by_id(db, complaint_id)

        if not complaint:
            raise ComplaintNotFoundError()

        if complaint.customer_id != customer_id:
            raise UnauthorizedComplaintAccessError(
                "You cannot upload an image for another customer's complaint"
            )

        if complaint.status != "PENDING":
            raise ComplaintNotEditableError(
                "Image can only be uploaded while the complaint is pending"
            )

        image_path: str = await upload_image(
            image,
            settings.COMPLAINT_UPLOAD_DIR,
        )

        return await self.complaint_repository.update_complaint_image(
            db, complaint, image_path
        )

    async def update_complaint(
        self,
        db: AsyncSession,
        complaint_id: int,
        customer_id: int,
        complaint_data: ComplaintUpdate,
    ) -> Complaint:
        complaint: (
            Complaint | None
        ) = await self.complaint_repository.get_complaint_by_id(db, complaint_id)

        if not complaint:
            raise ComplaintNotFoundError()

        if complaint.customer_id != customer_id:
            raise UnauthorizedComplaintAccessError(
                "You are not allowed to update this complaint"
            )

        if complaint.status != "PENDING":
            raise ComplaintNotEditableError("Only pending complaints can be updated")

        update_data = complaint_data.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(
                status_code=400,
                detail="No fields provided for update",
            )

        return await self.complaint_repository.update_complaint(
            db,
            complaint,
            update_data,
        )
