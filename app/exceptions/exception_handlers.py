from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status

from app.exceptions.custom_exceptions.employee_exceptions import (
    EmployeeNotFoundError,
    EmployeeAlreadyExistsError,
    EmployeeAlreadyInactiveError,
    InvalidEmployeeRoleError,
)
from app.exceptions.custom_exceptions.customer_exceptions import (
    CustomerNotFoundError,
    CustomerAlreadyExistsError,
    CustomerAlreadyInactiveError,
)
from app.exceptions.custom_exceptions.complaint_exceptions import (
    ComplaintNotFoundError,
    ComplaintAlreadyExistsError,
    ComplaintAlreadyAssignedError,
    ComplaintNotEditableError,
    ComplaintNotReadyToCloseError,
    UnauthorizedComplaintAccessError,
)
from app.exceptions.custom_exceptions.repair_exceptions import (
    RepairNotFoundError,
    RepairAlreadyExistsError,
    RepairNotAssignedError,
    RepairNotAllowedError,
    RepairAlreadyCompletedError,
)
from app.exceptions.custom_exceptions.assignment_exceptions import (
    AssignmentNotFoundError,
    AssignmentAlreadyExistsError,
    InvalidLinemanAssignmentError,
)

from app.exceptions.custom_exceptions.base_exception import BaseCustomException

logger: logging.Logger = logging.getLogger(__name__)
async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    logger.warning(
        "HTTP exception: %s | Path: %s | Status: %s",
        exc.detail,
        request.url.path,
        exc.status_code,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
        },
    )

async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    logger.warning(
        "Request validation failed | Path: %s | Errors: %s",
        request.url.path,
        exc.errors(),
    )
     
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation failed",
            "errors": exc.errors(),
        },
    )

async def database_exception_handler(
    request: Request,
    exc: SQLAlchemyError,
) -> JSONResponse:
    logger.exception("Database error occurred")

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "A database error occurred",
        },
    )

async def general_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    logger.exception("Unexpected error occurred")

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
        },
    )

async def custom_exception_handler(
    request: Request,
    exc: BaseCustomException,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
        },
    )
