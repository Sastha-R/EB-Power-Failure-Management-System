from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class CustomerRepositoryInterface(ABC):
    @abstractmethod
    async def create_customer(self, db: AsyncSession, customer_data: dict):
        pass

    @abstractmethod
    async def get_customer_by_id(self, db: AsyncSession, customer_id: int):
        pass

    @abstractmethod
    async def get_customer_by_email(self, db: AsyncSession, email: str):
        pass

    @abstractmethod
    async def get_customer_by_username(self, db: AsyncSession, username: str):
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
        customer,
    ):
        pass