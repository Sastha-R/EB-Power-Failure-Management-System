import jwt
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)
from app.repositories.implementations.customer_repository import CustomerRepository
from app.repositories.implementations.employee_repository import EmployeeRepository
from app.services.interfaces.auth_service_interface import AuthServiceInterface


class AuthService(AuthServiceInterface):
    def __init__(
        self,
        employee_repository: EmployeeRepository,
        customer_repository: CustomerRepository,
    ):
        self.employee_repository = employee_repository
        self.customer_repository = customer_repository

    async def employee_login(self, db: AsyncSession, email: str, password: str):
        employee = await self.employee_repository.get_employee_by_email(db, email)

        if employee:
            if not verify_password(password, employee.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password",
                )

            if not employee.is_active:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Employee account is inactive",
                )

            return {
                "access_token": create_access_token(
                    user_id=employee.id, user_type="employee", role=employee.role
                ),
                "refresh_token": create_refresh_token(
                    user_id=employee.id, user_type="employee", role=employee.role
                ),
                "token_type": "bearer",
            }

        return await self.customer_login(db, email, password)

    async def refresh_access_token(self, db: AsyncSession, refresh_token: str):
        try:
            payload = decode_token(refresh_token)

            if payload.get("token_type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token",
                )

            user_id = int(payload.get("sub"))
            user_type = payload.get("user_type")

        except (jwt.InvalidTokenError, ValueError, TypeError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
            )

        if user_type == "employee":
            user = await self.employee_repository.get_employee_by_id(db, user_id)

            if user and user.is_active:
                new_access_token = create_access_token(
                    user_id=user.id, user_type="employee", role=user.role
                )
            else:
                user = None

        elif user_type == "customer":
            user = await self.customer_repository.get_customer_by_id(db, user_id)

            if user and user.is_active:
                new_access_token = create_access_token(
                    user_id=user.id, user_type="customer"
                )
            else:
                user = None

        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user type"
            )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
            )

        return {"access_token": new_access_token, "token_type": "bearer"}

    async def customer_login(self, db: AsyncSession, email: str, password: str):
        customer = await self.customer_repository.get_customer_by_email(db, email)

        if not customer or not verify_password(password, customer.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not customer.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Customer account is inactive",
            )

        access_token = create_access_token(user_id=customer.id, user_type="customer")

        refresh_token = create_refresh_token(user_id=customer.id, user_type="customer")

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
