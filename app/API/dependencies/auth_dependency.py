from typing import Annotated, Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.database.database import get_db
from app.models.customer import Customer
from app.models.employee import Employee
from app.repositories.implementations.customer_repository import CustomerRepository
from app.repositories.implementations.employee_repository import EmployeeRepository

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_employee(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Employee:
    try:
        payload: dict[str, Any] = decode_token(token)

        if payload.get("token_type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token"
            )

        if payload.get("user_type") != "employee":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Employee access required"
            )

        employee_id: int = int(payload.get("sub"))

    except (jwt.InvalidTokenError, ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )

    repository: EmployeeRepository = EmployeeRepository()
    employee: Employee | None = await repository.get_employee_by_id(db, employee_id)

    if not employee or not employee.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Employee not found or inactive",
        )

    return employee


async def required_admin(
    current_employee: Annotated[Employee, Depends(get_current_employee)],
) -> Employee:
    if current_employee.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )

    return current_employee


async def get_current_customer(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Customer:
    try:
        payload: dict[str, Any] = decode_token(token)

        if payload.get("token_type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token"
            )

        if payload.get("user_type") != "customer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Customer access required"
            )

        customer_id: int = int(payload.get("sub"))

    except (jwt.InvalidTokenError, ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )

    customer_repository: CustomerRepository = CustomerRepository()

    customer: Customer | None = await customer_repository.get_customer_by_id(
        db, customer_id
    )

    if not customer or not customer.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Customer not found or inactive",
        )

    return customer


async def required_lineman(
    current_employee: Annotated[Employee, Depends(get_current_employee)],
) -> Employee:
    if current_employee.role != "lineman":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Lineman access required"
        )

    return current_employee
