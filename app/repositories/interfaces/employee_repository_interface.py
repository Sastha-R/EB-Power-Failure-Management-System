from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class EmployeeRepositoryInterface(ABC):
    @abstractmethod
    async def create_employee(self, db: AsyncSession, employee_data: dict):
        pass

    @abstractmethod
    async def get_employee_by_id(self, db: AsyncSession, employee_id: int):
        pass

    @abstractmethod
    async def get_employee_by_email(self, db: AsyncSession, email: str):
        pass

    @abstractmethod
    async def get_employee_by_username(self, db: AsyncSession, username: str):
        pass

    @abstractmethod
    async def get_all_employees(self, db: AsyncSession):
        pass
