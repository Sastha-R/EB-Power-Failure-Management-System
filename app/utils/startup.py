import logging

from sqlalchemy import select
from app.database.database import SessionLocal
from app.models import Employee

logger = logging.getLogger(__name__)


async def check_admin_exists():
    async with SessionLocal() as db:
        result = await db.execute(
            select(Employee).where(
                Employee.role == "admin",
                Employee.is_active.is_(True),
            )
        )

        admin = result.scalar_one_or_none()

        if admin:
            logger.info("Active admin account exists")
        else:
            logger.warning(
                "No active admin account found. "
                "Please create an admin using the admin creation script."
            )