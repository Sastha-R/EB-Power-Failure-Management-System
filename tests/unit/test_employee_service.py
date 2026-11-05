from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app.core.security import verify_password
from app.exceptions.custom_exceptions.employee_exceptions import (
    EmployeeAlreadyExistsError,
    EmployeeAlreadyInactiveError,
)
from app.services.implementations.employee_service import EmployeeService


@pytest.mark.asyncio
@pytest.mark.unit
async def test_create_employee_hashes_password_and_sets_lineman(
    mock_repository: MagicMock,
) -> None:
    data: SimpleNamespace = SimpleNamespace(
        email="a@example.com",
        username="lineman",
        model_dump=lambda: {
            "email": "a@example.com",
            "username": "lineman",
            "password": "password1",
        },
    )
    mock_repository.get_employee_by_email.return_value = None
    mock_repository.get_employee_by_username.return_value = None
    mock_repository.create_employee.side_effect = lambda db, row: row
    result: dict[str, object] = await EmployeeService(
        mock_repository
    ).create_employee(None, data)
    assert result["role"] == "lineman" and result["employee_code"].startswith("EMP")
    assert verify_password("password1", result["password"])


@pytest.mark.asyncio
@pytest.mark.unit
async def test_create_employee_rejects_duplicate_email(
    mock_repository: MagicMock,
) -> None:
    mock_repository.get_employee_by_email.return_value = object()
    data: SimpleNamespace = SimpleNamespace(email="a@example.com", username="x")
    with pytest.raises(EmployeeAlreadyExistsError):
        await EmployeeService(mock_repository).create_employee(None, data)


@pytest.mark.asyncio
@pytest.mark.unit
async def test_deactivate_employee_marks_active_employee_inactive(
    mock_repository: MagicMock,
) -> None:
    employee: SimpleNamespace = SimpleNamespace(id=1, is_active=True)
    mock_repository.get_employee_by_id.return_value = employee
    mock_repository.deactivate_employee.return_value = employee
    assert (
        await EmployeeService(mock_repository).deactivate_employee(None, 1) is employee
    )
    mock_repository.deactivate_employee.assert_awaited_once_with(None, employee)


@pytest.mark.asyncio
@pytest.mark.unit
async def test_deactivate_employee_rejects_already_inactive(
    mock_repository: MagicMock,
) -> None:
    mock_repository.get_employee_by_id.return_value = SimpleNamespace(is_active=False)
    with pytest.raises(EmployeeAlreadyInactiveError):
        await EmployeeService(mock_repository).deactivate_employee(None, 1)
