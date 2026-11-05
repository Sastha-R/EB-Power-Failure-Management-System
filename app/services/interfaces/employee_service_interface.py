from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.employee import Employee
from app.schemas.employee_schema import EmployeeCreate


class EmployeeServiceInterface(ABC):
    @abstractmethod
    async def create_employee(
        self, db: AsyncSession, employee_data: EmployeeCreate
    ) -> Employee:
        pass

    @abstractmethod
    async def get_employee_by_id(
        self, db: AsyncSession, employee_id: int
    ) -> Employee:
        pass

    @abstractmethod
    async def get_all_employees(
        self,
        db: AsyncSession,
        limit: int,
        offset: int,
    ) -> list[Employee]:
        pass

    @abstractmethod
    async def deactivate_employee(
        self,
        db: AsyncSession,
        employee_id: int,
    ) -> Employee:
        pass
