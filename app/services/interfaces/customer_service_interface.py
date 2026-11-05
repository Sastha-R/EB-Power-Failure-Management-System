from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer
from app.schemas.customer_schema import CustomerCreate


class CustomerServiceInterface(ABC):
    @abstractmethod
    async def create_customer(
        self, db: AsyncSession, customer_data: CustomerCreate
    ) -> Customer:
        pass

    @abstractmethod
    async def get_customer_by_id(self, db: AsyncSession, customer_id: int) -> Customer:
        pass

    @abstractmethod
    async def get_all_customers(
        self,
        db: AsyncSession,
        limit: int,
        offset: int,
    ) -> list[Customer]:
        pass

    @abstractmethod
    async def deactivate_customer(
        self,
        db: AsyncSession,
        customer_id: int,
    ) -> Customer:
        pass
