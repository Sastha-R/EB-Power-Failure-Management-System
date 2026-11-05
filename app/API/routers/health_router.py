from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.health_dependency import get_health_service
from app.database.database import get_db
from app.services.implementations.health_service import HealthService

health_router: APIRouter = APIRouter(
    prefix="/health",
    tags=["Health Check"],
)


@health_router.get("/")
async def health_check(
    db: Annotated[AsyncSession, Depends(get_db)],
    health_service: Annotated[HealthService, Depends(get_health_service)],
) -> dict[str, str]:
    return await health_service.check_health(db)
