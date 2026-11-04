from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class EmployeeServiceInterface(ABC):
    @abstractmethod
    async def create_employee(self, db: AsyncSession, employee_data):
        pass

    @abstractmethod
    async def get_employee_by_id(self, db: AsyncSession, employee_id: int):
        pass

    @abstractmethod
    async def get_all_employees(
        self,
        db: AsyncSession,
        limit: int,
        offset: int,
    ):
        pass

    @abstractmethod
    async def deactivate_employee(
        self,
        db: AsyncSession,
        employee_id: int,
    ):
        pass