import jwt
import pytest
from typing import Any

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)


@pytest.mark.unit
def test_password_hash_is_verified_and_not_plaintext() -> None:
    hashed: str = hash_password("safe-password")
    assert hashed != "safe-password"
    assert verify_password("safe-password", hashed)
    assert not verify_password("wrong-password", hashed)


@pytest.mark.unit
def test_access_and_refresh_tokens_have_distinct_types() -> None:
    access: dict[str, Any] = decode_token(
        create_access_token(7, "employee", "lineman")
    )
    refresh: dict[str, Any] = decode_token(
        create_refresh_token(7, "employee", "lineman")
    )
    assert (
        access["sub"],
        access["user_type"],
        access["role"],
        access["token_type"],
    ) == ("7", "employee", "lineman", "access")
    assert refresh["token_type"] == "refresh"


@pytest.mark.unit
def test_decode_rejects_invalid_token() -> None:
    with pytest.raises(jwt.InvalidTokenError):
        decode_token("not-a-jwt")
