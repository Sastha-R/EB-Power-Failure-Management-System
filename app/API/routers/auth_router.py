from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.API.dependencies.auth_service_dependency import get_auth_service
from app.services.implementations.auth_service import AuthService
from app.schemas.auth_schema import TokenResponse


auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@auth_router.post("/login", response_model=TokenResponse)
async def employee_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.employee_login(
        db,
        form_data.username,
        form_data.password
    )