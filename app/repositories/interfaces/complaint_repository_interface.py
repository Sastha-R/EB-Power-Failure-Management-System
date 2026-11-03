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