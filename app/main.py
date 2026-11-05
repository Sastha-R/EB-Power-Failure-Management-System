from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.api.routers.auth_router import auth_router
from app.api.routers.complaint_router import complaint_router
from app.api.routers.complaint_report_router import complaint_report_router
from app.api.routers.customer_router import customer_router
from app.api.routers.employee_router import employee_router
from app.api.routers.health_router import health_router
from app.api.routers.repair_router import repair_router
from app.utils.logging_config import setup_logging
from app.exceptions.custom_exceptions.base_exception import BaseCustomException
from app.exceptions.exception_handlers import (
    custom_exception_handler,
    database_exception_handler,
    general_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from app.middleware.request_logging_middleware import (
    RequestLoggingMiddleware,
)
from contextlib import asynccontextmanager
import logging
from app.database.database import engine
from app.utils.startup import check_admin_exists

from app.exceptions.exception_registration import (
    register_exception_handlers,
)

setup_logging()
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger = logging.getLogger(__name__)

    logger.info("Application starting")

    await check_admin_exists()

    yield

    await engine.dispose()

    logger.info("Application shutdown completed")






app = FastAPI(
    title="EB Power Failure Management System",
    lifespan=lifespan
    )

app.add_middleware(RequestLoggingMiddleware)


register_exception_handlers(app)


app.include_router(employee_router)
app.include_router(auth_router)
app.include_router(customer_router)
app.include_router(complaint_router)
app.include_router(complaint_report_router)
app.include_router(repair_router)
app.include_router(health_router)
