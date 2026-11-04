import logging
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.exceptions.custom_exceptions.employee_exceptions import (
    EmployeeAlreadyExistsError,
    EmployeeAlreadyInactiveError,
    EmployeeNotFoundError,
)
from app.repositories.implementations.employee_repository import EmployeeRepository
from app.services.interfaces.employee_service_interface import EmployeeServiceInterface

logger = logging.getLogger(__name__)


class EmployeeService(EmployeeServiceInterface):
    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository

    async def create_employee(self, db: AsyncSession, employee_data):

        existing_email = await self.employee_repository.get_employee_by_email(
            db, employee_data.email
        )

        if existing_email:
            raise EmployeeAlreadyExistsError("Email already registered")

        existing_username = await self.employee_repository.get_employee_by_username(
            db, employee_data.username
        )

        if existing_username:
            raise EmployeeAlreadyExistsError(
                "Employee with this username already exists"
            )

        employee_dict = employee_data.model_dump()

        employee_dict["password"] = hash_password(employee_dict["password"])

        employee_dict["employee_code"] = f"EMP{uuid.uuid4().hex[:8].upper()}"

        employee_dict["role"] = "lineman"

        return await self.employee_repository.create_employee(db, employee_dict)

    async def get_employee_by_id(self, db: AsyncSession, employee_id: int):

        employee = await self.employee_repository.get_employee_by_id(db, employee_id)

        if not employee:
            raise EmployeeNotFoundError()

        return employee

    async def get_all_employees(self, db: AsyncSession):

        return await self.employee_repository.get_all_employees(db)

    async def deactivate_employee(
        self,
        db: AsyncSession,
        employee_id: int,
    ):
        employee = await self.employee_repository.get_employee_by_id(db, employee_id)

        if not employee:
            logger.warning(
                "Employee with ID %s not found",
                employee_id,
            )
            raise EmployeeNotFoundError()

        if not employee.is_active:
            logger.warning("Employee with ID %s is already inactive", employee_id)
            raise EmployeeAlreadyInactiveError()

        result = await self.employee_repository.deactivate_employee(db, employee)

        logger.info(
            "Employee with ID %s deactivated successfully",
            employee_id,
        )

        return result
