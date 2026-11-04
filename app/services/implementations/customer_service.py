import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.exceptions.custom_exceptions.customer_exceptions import (
    CustomerAlreadyExistsError,
    CustomerNotFoundError,
)
from app.repositories.implementations.customer_repository import CustomerRepository
from app.services.interfaces.customer_service_interface import CustomerServiceInterface
from app.exceptions.custom_exceptions.customer_exceptions import (
    CustomerNotFoundError,
    CustomerAlreadyInactiveError,
)

class CustomerService(CustomerServiceInterface):
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    async def create_customer(self, db: AsyncSession, customer_data):

        existing_email = await self.customer_repository.get_customer_by_email(
            db, customer_data.email
        )

        if existing_email:
            raise CustomerAlreadyExistsError("Customer with this email already exists")

        existing_username = await self.customer_repository.get_customer_by_username(
            db, customer_data.username
        )

        if existing_username:
            raise CustomerAlreadyExistsError(
                "Customer with this username already exists"
            )

        customer_dict = customer_data.model_dump()

        customer_dict["password"] = hash_password(customer_dict["password"])
        customer_dict["customer_code"] = f"CUS{uuid.uuid4().hex[:8].upper()}"

        return await self.customer_repository.create_customer(db, customer_dict)

    async def get_customer_by_id(self, db: AsyncSession, customer_id: int):

        customer = await self.customer_repository.get_customer_by_id(db, customer_id)

        if not customer:
            raise CustomerNotFoundError()

        return customer

    async def get_all_customers(
        self,
        db: AsyncSession,
        limit: int,
        offset: int,
    ):
        return await self.customer_repository.get_all_customers(
            db,
            limit,
            offset,
        )


    async def deactivate_customer(
        self,
        db: AsyncSession,
        customer_id: int,
    ):
        customer = await self.customer_repository.get_customer_by_id(
            db,
            customer_id,
        )

        if not customer:
            raise CustomerNotFoundError()

        if not customer.is_active:
            raise CustomerAlreadyInactiveError()

        return await self.customer_repository.deactivate_customer(
            db,
            customer,
        )