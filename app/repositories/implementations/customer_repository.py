from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Customer
from app.repositories.interfaces.customer_repository_interface import (
    CustomerRepositoryInterface,
)


class CustomerRepository(CustomerRepositoryInterface):
    async def create_customer(
        self, db: AsyncSession, customer_data: dict[str, object]
    ) -> Customer:

        customer: Customer = Customer(**customer_data)

        db.add(customer)
        await db.commit()
        await db.refresh(customer)

        return customer

    async def get_customer_by_id(
        self, db: AsyncSession, customer_id: int
    ) -> Customer | None:

        result = await db.execute(select(Customer).where(Customer.id == customer_id))

        return result.scalar_one_or_none()

    async def get_customer_by_email(
        self, db: AsyncSession, email: str
    ) -> Customer | None:

        result = await db.execute(select(Customer).where(Customer.email == email))

        return result.scalar_one_or_none()

    async def get_customer_by_username(
        self, db: AsyncSession, username: str
    ) -> Customer | None:

        result = await db.execute(select(Customer).where(Customer.username == username))

        return result.scalar_one_or_none()

    async def get_all_customers(
        self,
        db: AsyncSession,
        limit: int,
        offset: int,
    ) -> list[Customer]:
        result = await db.execute(select(Customer).limit(limit).offset(offset))

        return result.scalars().all()

    async def deactivate_customer(
        self,
        db: AsyncSession,
        customer: Customer,
    ) -> Customer:
        customer.is_active = False

        await db.commit()
        await db.refresh(customer)

        return customer
