from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth_service_dependency import get_auth_service
from app.database.database import get_db
from app.schemas.auth_schema import RefreshTokenRequest, TokenResponse
from app.services.implementations.auth_service import AuthService

auth_router: APIRouter = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/login", response_model=TokenResponse)
async def employee_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> TokenResponse:
    return await auth_service.employee_login(db, form_data.username, form_data.password)


@auth_router.post("/refresh")
async def refresh_access_token(
    refresh_data: RefreshTokenRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> dict[str, str]:
    return await auth_service.refresh_access_token(db, refresh_data.refresh_token)
