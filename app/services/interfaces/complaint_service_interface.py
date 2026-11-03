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

    