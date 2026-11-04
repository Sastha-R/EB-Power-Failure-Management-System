from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.api.dependencies.health_dependency import get_health_service
from app.services.implementations.health_service import HealthService


health_router = APIRouter(
    prefix="/health",
    tags=["Health Check"],
)


@health_router.get("/")
async def health_check(
    db: AsyncSession = Depends(get_db),
    health_service: HealthService = Depends(get_health_service),
):
    return await health_service.check_health(db)