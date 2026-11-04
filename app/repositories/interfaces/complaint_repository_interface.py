from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class ComplaintRepositoryInterface(ABC):

    @abstractmethod
    async def create_complaint(
        self,
        db: AsyncSession,
        complaint_data: dict
    ):
        pass


    @abstractmethod
    async def get_customer_complaints(
        self,
        db: AsyncSession,
        customer_id: int
    ):
        pass

    @abstractmethod
    async def get_all_complaints(
        self,
        db: AsyncSession
    ):
        pass

    @abstractmethod
    async def assign_complaint(
        self,
        db: AsyncSession,
        assignment_data: dict
    ):
        pass

    @abstractmethod
    async def get_complaint_by_id(
        self,
        db: AsyncSession,
        complaint_id: int
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
    async def close_complaint(self, db, complaint):
        pass

    @abstractmethod
    async def update_complaint_image(self, db, complaint, image_path: str):
        pass

    @abstractmethod
    async def update_complaint(
        self,
        db: AsyncSession,
        complaint,
        complaint_data: dict,
    ):
        pass