from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth_dependency import required_admin
from app.api.dependencies.customer_dependency import get_customer_service
from app.database.database import get_db
from app.schemas.customer_schema import CustomerCreate, CustomerResponse
from app.services.implementations.customer_service import CustomerService

customer_router = APIRouter(prefix="/customers", tags=["Customers"])


@customer_router.post(
    "/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED
)
async def create_customer(
    customer_data: CustomerCreate,
    db: AsyncSession = Depends(get_db),
    customer_service: CustomerService = Depends(get_customer_service),
):
    return await customer_service.create_customer(db, customer_data)


@customer_router.get("/", response_model=list[CustomerResponse])
async def get_all_customers(
    db: AsyncSession = Depends(get_db),
    customer_service: CustomerService = Depends(get_customer_service),
    current_admin=Depends(required_admin),
):
    return await customer_service.get_all_customers(db)


@customer_router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer_by_id(
    customer_id: int,
    db: AsyncSession = Depends(get_db),
    customer_service: CustomerService = Depends(get_customer_service),
    current_admin=Depends(required_admin),
):
    return await customer_service.get_customer_by_id(db, customer_id)
