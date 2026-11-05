from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Employee
from app.repositories.interfaces.employee_repository_interface import (
    EmployeeRepositoryInterface,
)


class EmployeeRepository(EmployeeRepositoryInterface):
    async def create_employee(
        self, db: AsyncSession, employee_data: dict[str, object]
    ) -> Employee:
        employee: Employee = Employee(**employee_data)

        db.add(employee)

        await db.commit()

        await db.refresh(employee)

        return employee

    async def get_employee_by_id(
        self, db: AsyncSession, employee_id: int
    ) -> Employee | None:
        result = await db.execute(select(Employee).where(Employee.id == employee_id))

        return result.scalar_one_or_none()

    async def get_employee_by_email(
        self, db: AsyncSession, email: str
    ) -> Employee | None:
        result = await db.execute(select(Employee).where(Employee.email == email))

        return result.scalar_one_or_none()

    async def get_employee_by_username(
        self, db: AsyncSession, username: str
    ) -> Employee | None:
        result = await db.execute(select(Employee).where(Employee.username == username))

        return result.scalar_one_or_none()

    async def get_all_employees(
        self,
        db: AsyncSession,
        limit: int,
        offset: int,
    ) -> list[Employee]:
        result = await db.execute(select(Employee).limit(limit).offset(offset))

        return result.scalars().all()

    async def deactivate_employee(
        self,
        db: AsyncSession,
        employee: Employee,
    ) -> Employee:
        employee.is_active = False

        await db.commit()
        await db.refresh(employee)

        return employee
