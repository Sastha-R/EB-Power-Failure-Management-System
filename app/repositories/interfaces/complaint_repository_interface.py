from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.complaint import Complaint
from app.models.complaint_assignment import ComplaintAssignment


class ComplaintRepositoryInterface(ABC):
    @abstractmethod
    async def create_complaint(
        self, db: AsyncSession, complaint_data: dict[str, object]
    ) -> Complaint:
        pass

    @abstractmethod
    async def get_customer_complaints(
        self, db: AsyncSession, customer_id: int
    ) -> list[Complaint]:
        pass

    @abstractmethod
    async def get_all_complaints(self, db: AsyncSession) -> list[Complaint]:
        pass

    @abstractmethod
    async def assign_complaint(
        self, db: AsyncSession, assignment_data: dict[str, object]
    ) -> ComplaintAssignment:
        pass

    @abstractmethod
    async def get_complaint_by_id(
        self, db: AsyncSession, complaint_id: int
    ) -> Complaint | None:
        pass

    @abstractmethod
    async def get_assigned_complaints(
        self, db: AsyncSession, lineman_id: int
    ) -> list[Complaint]:
        pass

    @abstractmethod
    async def close_complaint(
        self, db: AsyncSession, complaint: Complaint
    ) -> Complaint:
        pass

    @abstractmethod
    async def update_complaint_image(
        self, db: AsyncSession, complaint: Complaint, image_path: str
    ) -> Complaint:
        pass

    @abstractmethod
    async def update_complaint(
        self,
        db: AsyncSession,
        complaint: Complaint,
        complaint_data: dict[str, object],
    ) -> Complaint:
        pass
