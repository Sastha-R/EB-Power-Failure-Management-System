from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.implementations.employee_repository import EmployeeRepository
from app.services.interfaces.auth_service_interface import AuthServiceInterface
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token
)
import jwt
from app.core.security import decode_token


class AuthService(AuthServiceInterface):

    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository

    async def employee_login(
        self,
        db: AsyncSession,
        email: str,
        password: str
    ):
        employee = await self.employee_repository.get_employee_by_email(
            db, email
        )

        if not employee or not verify_password(password, employee.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not employee.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Employee account is inactive"
            )

        access_token = create_access_token(
            user_id=employee.id,
            user_type="employee",
            role=employee.role
        )

        refresh_token = create_refresh_token(
            user_id=employee.id,
            user_type="employee",
            role=employee.role
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    async def refresh_access_token(
    self,
    db: AsyncSession,
    refresh_token: str
    ):
        try:
            payload = decode_token(refresh_token)

            if payload.get("token_type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token"
                )

            if payload.get("user_type") != "employee":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid user type"
                )

            employee_id = int(payload.get("sub"))

        except (jwt.InvalidTokenError, ValueError, TypeError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )

        employee = await self.employee_repository.get_employee_by_id(
            db, employee_id
        )

        if not employee or not employee.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Employee not found or inactive"
            )

        new_access_token = create_access_token(
            user_id=employee.id,
            user_type="employee",
            role=employee.role
        )

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }