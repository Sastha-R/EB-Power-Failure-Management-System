from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.schemas.employee_schema import EmployeeCreate, EmployeeResponse
from app.services.implementations.employee_service import EmployeeService
from app.API.dependencies.employee_dependency import get_employee_service
from app.API.dependencies.auth_dependency import required_admin


employee_router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


@employee_router.post(
    "/",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_employee(
    employee_data: EmployeeCreate,
    db: AsyncSession = Depends(get_db),
    employee_service: EmployeeService = Depends(get_employee_service),
    current_admin=Depends(required_admin)
):
    return await employee_service.create_employee(db, employee_data)


@employee_router.get(
    "/",
    response_model=list[EmployeeResponse]
)
async def get_all_employees(
    db: AsyncSession = Depends(get_db),
    employee_service: EmployeeService = Depends(get_employee_service),
    current_admin=Depends(required_admin)
):
    return await employee_service.get_all_employees(db)


@employee_router.get(
    "/{employee_id}",
    response_model=EmployeeResponse
)
async def get_employee_by_id(
    employee_id: int,
    db: AsyncSession = Depends(get_db),
    employee_service: EmployeeService = Depends(get_employee_service),
    current_admin=Depends(required_admin)
):
    return await employee_service.get_employee_by_id(db, employee_id)