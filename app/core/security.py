from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from pwdlib import PasswordHash

from app.core.config import settings

password_hash: PasswordHash = PasswordHash.recommended()


# Password hashing
def hash_password(password: str) -> str:

    return password_hash.hash(password)


# Password verification
def verify_password(plain_password: str, hashed_password: str) -> bool:

    return password_hash.verify(plain_password, hashed_password)


# Access token generation
def create_access_token(user_id: int, user_type: str, role: str | None = None) -> str:

    expire: datetime = datetime.now(UTC) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload: dict[str, str | datetime] = {
        "sub": str(user_id),
        "user_type": user_type,
        "token_type": "access",
        "exp": expire,
    }

    if role:
        payload["role"] = role

    return jwt.encode(
        payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )


# Refresh token generation
def create_refresh_token(user_id: int, user_type: str, role: str | None = None) -> str:

    expire: datetime = datetime.now(UTC) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    payload: dict[str, str | datetime] = {
        "sub": str(user_id),
        "user_type": user_type,
        "token_type": "refresh",
        "exp": expire,
    }

    if role:
        payload["role"] = role

    return jwt.encode(
        payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )


# Token decoding
def decode_token(token: str) -> dict[str, Any]:

    return jwt.decode(
        token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
    )
