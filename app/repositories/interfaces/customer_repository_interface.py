from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer


class CustomerRepositoryInterface(ABC):
    @abstractmethod
    async def create_customer(
        self, db: AsyncSession, customer_data: dict[str, object]
    ) -> Customer:
        pass

    @abstractmethod
    async def get_customer_by_id(
        self, db: AsyncSession, customer_id: int
    ) -> Customer | None:
        pass

    @abstractmethod
    async def get_customer_by_email(
        self, db: AsyncSession, email: str
    ) -> Customer | None:
        pass

    @abstractmethod
    async def get_customer_by_username(
        self, db: AsyncSession, username: str
    ) -> Customer | None:
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
        customer: Customer,
    ) -> Customer:
        pass
