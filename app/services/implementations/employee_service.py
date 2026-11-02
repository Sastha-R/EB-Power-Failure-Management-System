import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.repositories.implementations.employee_repository import EmployeeRepository
from app.services.interfaces.employee_service_interface import EmployeeServiceInterface


class EmployeeService(EmployeeServiceInterface):
    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository

    async def create_employee(self, db: AsyncSession, employee_data):

        existing_email = await self.employee_repository.get_employee_by_email(
            db, employee_data.email
        )

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
            )

        existing_username = await self.employee_repository.get_employee_by_username(
            db, employee_data.username
        )

        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Username already exists"
            )

        employee_dict = employee_data.model_dump()

        employee_dict["password"] = hash_password(employee_dict["password"])

        employee_dict["employee_code"] = f"EMP{uuid.uuid4().hex[:8].upper()}"

        employee_dict["role"] = "lineman"

        return await self.employee_repository.create_employee(db, employee_dict)

    async def get_employee_by_id(self, db: AsyncSession, employee_id: int):

        employee = await self.employee_repository.get_employee_by_id(db, employee_id)

        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
            )

        return employee

    async def get_all_employees(self, db: AsyncSession):

        return await self.employee_repository.get_all_employees(db)
