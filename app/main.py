import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routers.auth_router import auth_router
from app.api.routers.complaint_report_router import complaint_report_router
from app.api.routers.complaint_router import complaint_router
from app.api.routers.customer_router import customer_router
from app.api.routers.employee_router import employee_router
from app.api.routers.health_router import health_router
from app.api.routers.repair_router import repair_router
from app.database.database import engine
from app.exceptions.exception_registration import (
    register_exception_handlers,
)
from app.middleware.request_logging_middleware import (
    RequestLoggingMiddleware,
)
from app.utils.logging_config import setup_logging
from app.utils.startup import check_admin_exists

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger: logging.Logger = logging.getLogger(__name__)

    logger.info("Application starting")

    await check_admin_exists()

    yield

    await engine.dispose()

    logger.info("Application shutdown completed")


app: FastAPI = FastAPI(title="EB Power Failure Management System", lifespan=lifespan)

app.add_middleware(RequestLoggingMiddleware)


register_exception_handlers(app)


app.include_router(employee_router)
app.include_router(auth_router)
app.include_router(customer_router)
app.include_router(complaint_router)
app.include_router(complaint_report_router)
app.include_router(repair_router)
app.include_router(health_router)
