from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.repositories.implementations.employee_repository import EmployeeRepository
from app.core.security import decode_token
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")



async def get_current_employee(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    try:
        payload = decode_token(token)

        if payload.get("token_type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token"
            )

        if payload.get("user_type") != "employee":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Employee access required"
            )

        employee_id = int(payload.get("sub"))

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    repository = EmployeeRepository()
    employee = await repository.get_employee_by_id(db, employee_id)

    if not employee or not employee.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Employee not found or inactive"
        )

    return employee


async def required_admin(
    current_employee=Depends(get_current_employee)
):
    if current_employee.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_employee