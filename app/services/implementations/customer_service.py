import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.repositories.implementations.customer_repository import CustomerRepository
from app.services.interfaces.customer_service_interface import CustomerServiceInterface


class CustomerService(CustomerServiceInterface):
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    async def create_customer(self, db: AsyncSession, customer_data):

        existing_email = await self.customer_repository.get_customer_by_email(
            db, customer_data.email
        )

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
            )

        existing_username = await self.customer_repository.get_customer_by_username(
            db, customer_data.username
        )

        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Username already exists"
            )

        customer_dict = customer_data.model_dump()

        customer_dict["password"] = hash_password(customer_dict["password"])
        customer_dict["customer_code"] = f"CUS{uuid.uuid4().hex[:8].upper()}"

        return await self.customer_repository.create_customer(db, customer_dict)

    async def get_customer_by_id(self, db: AsyncSession, customer_id: int):

        customer = await self.customer_repository.get_customer_by_id(db, customer_id)

        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
            )

        return customer

    async def get_all_customers(self, db: AsyncSession):

        return await self.customer_repository.get_all_customers(db)
