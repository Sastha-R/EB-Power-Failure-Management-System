from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app.core.security import verify_password
from app.exceptions.custom_exceptions.customer_exceptions import (
    CustomerAlreadyExistsError,
    CustomerAlreadyInactiveError,
)
from app.services.implementations.customer_service import CustomerService


@pytest.mark.asyncio
@pytest.mark.unit
async def test_register_customer_hashes_password(
    mock_repository: MagicMock,
) -> None:
    data: SimpleNamespace = SimpleNamespace(
        email="c@example.com",
        username="customer",
        model_dump=lambda: {
            "email": "c@example.com",
            "username": "customer",
            "password": "password1",
        },
    )
    mock_repository.get_customer_by_email.return_value = None
    mock_repository.get_customer_by_username.return_value = None
    mock_repository.create_customer.side_effect = lambda db, row: row
    result: dict[str, object] = await CustomerService(
        mock_repository
    ).create_customer(None, data)
    assert result["customer_code"].startswith("CUS")
    assert verify_password("password1", result["password"])


@pytest.mark.asyncio
@pytest.mark.unit
async def test_register_customer_rejects_duplicate(
    mock_repository: MagicMock,
) -> None:
    mock_repository.get_customer_by_email.return_value = object()
    with pytest.raises(CustomerAlreadyExistsError):
        await CustomerService(mock_repository).create_customer(
            None, SimpleNamespace(email="x", username="x")
        )


@pytest.mark.asyncio
@pytest.mark.unit
async def test_deactivate_customer_rejects_already_inactive(
    mock_repository: MagicMock,
) -> None:
    mock_repository.get_customer_by_id.return_value = SimpleNamespace(is_active=False)
    with pytest.raises(CustomerAlreadyInactiveError):
        await CustomerService(mock_repository).deactivate_customer(None, 1)
