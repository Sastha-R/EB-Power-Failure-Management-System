import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.employee import Employee
from app.repositories.implementations.employee_repository import EmployeeRepository


@pytest.mark.integration
@pytest.mark.asyncio
async def test_employee_repository_create_lookup_and_deactivate(
    db_session: AsyncSession,
) -> None:
    repository: EmployeeRepository = EmployeeRepository()
    employee: Employee = await repository.create_employee(
        db_session,
        {
            "employee_code": "EMPINT0001",
            "username": "employee_integration",
            "email": "employee.integration@example.com",
            "password": "hashed-password",
            "role": "lineman",
            "phone_number": "9876543210",
            "door_no": "10",
            "street": "Integration Road",
            "district": "Test District",
            "pincode": "600001",
        },
    )

    found: Employee | None = await repository.get_employee_by_email(
        db_session, employee.email
    )
    deactivated: Employee = await repository.deactivate_employee(db_session, employee)

    assert found is not None
    assert found.id == employee.id
    assert deactivated.is_active is False
