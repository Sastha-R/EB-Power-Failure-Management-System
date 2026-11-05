from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.employee import Employee


class EmployeeRepositoryInterface(ABC):
    @abstractmethod
    async def create_employee(
        self, db: AsyncSession, employee_data: dict[str, object]
    ) -> Employee:
        pass

    @abstractmethod
    async def get_employee_by_id(
        self, db: AsyncSession, employee_id: int
    ) -> Employee | None:
        pass

    @abstractmethod
    async def get_employee_by_email(
        self, db: AsyncSession, email: str
    ) -> Employee | None:
        pass

    @abstractmethod
    async def get_employee_by_username(
        self, db: AsyncSession, username: str
    ) -> Employee | None:
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
        employee: Employee,
    ) -> Employee:
        pass
