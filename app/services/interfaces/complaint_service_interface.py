from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile

from app.models.complaint import Complaint
from app.schemas.complaint_schema import ComplaintCreate


class ComplaintServiceInterface(ABC):

    @abstractmethod
    async def create_complaint(
        self,
        db: AsyncSession,
        customer_id: int,
        complaint_data: ComplaintCreate,
    ) -> Complaint:
        pass

    @abstractmethod
    async def get_all_complaints(
        self,
        db: AsyncSession
    ) -> list[Complaint]:
        pass

    @abstractmethod
    async def get_assigned_complaints(
        self,
        db: AsyncSession,
        lineman_id: int
    ) -> list[Complaint]:
        pass

    @abstractmethod
    async def close_complaint(
        self, db: AsyncSession, complaint_id: int
    ) -> Complaint:
        pass

    @abstractmethod
    async def upload_complaint_image(
        self,
        db: AsyncSession,
        complaint_id: int,
        customer_id: int,
        image: UploadFile,
    ) -> Complaint:
        pass
