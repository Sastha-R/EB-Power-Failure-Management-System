from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class CustomerAuthRepositoryInterface(ABC):
    @abstractmethod
    async def get_customer_by_email(self, db: AsyncSession, email: str):
        pass

    @abstractmethod
    async def get_customer_by_id(self, db: AsyncSession, customer_id: int):
        pass
