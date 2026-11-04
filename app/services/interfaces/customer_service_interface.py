from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class CustomerServiceInterface(ABC):
    @abstractmethod
    async def create_customer(self, db: AsyncSession, customer_data):
        pass

    @abstractmethod
    async def get_customer_by_id(self, db: AsyncSession, customer_id: int):
        pass

    @abstractmethod
    async def get_all_customers(
        self,
        db: AsyncSession,
        limit: int,
        offset: int,
    ):
        pass

    @abstractmethod
    async def deactivate_customer(
        self,
        db: AsyncSession,
        customer_id: int,
    ):
        pass