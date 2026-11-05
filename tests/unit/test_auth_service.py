from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.core.security import create_refresh_token, decode_token, hash_password
from app.services.implementations.auth_service import AuthService


@pytest.mark.asyncio
@pytest.mark.unit
async def test_employee_login_returns_access_and_refresh_tokens(mock_repository):
    mock_repository.get_employee_by_email.return_value = SimpleNamespace(
        id=9, password=hash_password("password1"), is_active=True, role="lineman"
    )
    result = await AuthService(mock_repository, mock_repository).employee_login(
        None, "e@example.com", "password1"
    )
    assert decode_token(result["access_token"])["user_type"] == "employee"
    assert decode_token(result["refresh_token"])["token_type"] == "refresh"


@pytest.mark.asyncio
@pytest.mark.unit
async def test_customer_login_rejects_wrong_password(mock_repository):
    mock_repository.get_employee_by_email.return_value = None
    mock_repository.get_customer_by_email.return_value = SimpleNamespace(
        password=hash_password("correct-pass"), is_active=True
    )
    with pytest.raises(HTTPException) as error:
        await AuthService(mock_repository, mock_repository).employee_login(
            None, "c@example.com", "wrong-pass"
        )
    assert error.value.status_code == 401


@pytest.mark.asyncio
@pytest.mark.unit
async def test_refresh_token_issues_access_token(mock_repository):
    mock_repository.get_customer_by_id.return_value = SimpleNamespace(
        id=5, is_active=True
    )
    result = await AuthService(mock_repository, mock_repository).refresh_access_token(
        None, create_refresh_token(5, "customer")
    )
    assert decode_token(result["access_token"])["token_type"] == "access"
