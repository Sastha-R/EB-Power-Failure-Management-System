from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class ComplaintServiceInterface(ABC):

    @abstractmethod
    async def create_complaint(
        self,
        db: AsyncSession,
        customer_id: int,
        complaint_data
    ):
        pass

    @abstractmethod
    async def get_all_complaints(
        self,
        db: AsyncSession
    ):
        pass

    @abstractmethod
    async def get_assigned_complaints(
        self,
        db: AsyncSession,
        lineman_id: int
    ):
        pass

    @abstractmethod
    async def close_complaint(self, db, complaint_id: int):
        pass

    @abstractmethod
    async def upload_complaint_image(
        self, db, complaint_id: int, customer_id: int, image
    ):
        pass