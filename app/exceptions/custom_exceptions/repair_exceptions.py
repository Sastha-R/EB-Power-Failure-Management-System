from fastapi import status

from app.exceptions.custom_exceptions.base_exception import (
    BaseCustomException,
)


class RepairNotFoundError(BaseCustomException):
    def __init__(self, message="Repair record not found"):
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class RepairAlreadyExistsError(BaseCustomException):
    def __init__(self, message="Repair record already exists"):
        super().__init__(message, status.HTTP_409_CONFLICT)


class RepairNotAssignedError(BaseCustomException):
    def __init__(self, message="This complaint is not assigned to you"):
        super().__init__(message, status.HTTP_403_FORBIDDEN)


class RepairNotAllowedError(BaseCustomException):
    def __init__(self, message="Repair is not allowed in the current status"):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class RepairAlreadyCompletedError(BaseCustomException):
    def __init__(self, message="Repair has already been submited"):
        super().__init__(message, status.HTTP_409_CONFLICT)