from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status


class HealthService:

    async def check_health(self, db: AsyncSession):
        try:
            await db.execute(text("SELECT 1"))

            return {
                "status": "healthy",
                "application": "running",
                "database": "connected",
            }

        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail={
                    "status": "unhealthy",
                    "application": "running",
                    "database": "disconnected",
                },
            )