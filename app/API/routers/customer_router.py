from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth_dependency import required_admin
from app.api.dependencies.customer_dependency import get_customer_service
from app.database.database import get_db
from app.schemas.customer_schema import CustomerCreate, CustomerResponse
from app.services.implementations.customer_service import CustomerService
from typing import Annotated
from app.models.employee import Employee
from app.api.dependencies.auth_dependency import required_admin
from fastapi import Query
customer_router: APIRouter = APIRouter(prefix="/customers", tags=["Customers"])


@customer_router.post(
    "/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED
)
async def create_customer(
    customer_data: CustomerCreate,
    db: Annotated[AsyncSession , Depends(get_db)],
    customer_service: Annotated[CustomerService , Depends(get_customer_service)],
) -> CustomerResponse:
    return await customer_service.create_customer(db, customer_data)


@customer_router.get("/")
async def get_all_customers(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
    customer_service: CustomerService = Depends(get_customer_service),
    current_admin: Employee = Depends(required_admin),
) :
    return await customer_service.get_all_customers(
        db,
        limit,
        offset,
    )


@customer_router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer_by_id(
    customer_id: int,
    db: Annotated[AsyncSession , Depends(get_db)],
    customer_service: Annotated[CustomerService , Depends(get_customer_service)],
    current_admin: Annotated[Employee, Depends(required_admin)]

) -> CustomerResponse:
    return await customer_service.get_customer_by_id(db, customer_id)


@customer_router.delete("/{customer_id}")
async def deactivate_customer(
    customer_id: int,
    db: AsyncSession = Depends(get_db),
    customer_service: CustomerService = Depends(get_customer_service),
    current_admin: Employee = Depends(required_admin),
) :
    return await customer_service.deactivate_customer(
        db,
        customer_id,
    )
