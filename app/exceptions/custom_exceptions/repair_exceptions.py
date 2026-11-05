from fastapi import status

from app.exceptions.custom_exceptions.base_exception import (
    BaseCustomException,
)


class RepairNotFoundError(BaseCustomException):
    def __init__(self, message: str = "Repair record not found") -> None:
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class RepairAlreadyExistsError(BaseCustomException):
    def __init__(self, message: str = "Repair record already exists") -> None:
        super().__init__(message, status.HTTP_409_CONFLICT)


class RepairNotAssignedError(BaseCustomException):
    def __init__(self, message: str = "This complaint is not assigned to you") -> None:
        super().__init__(message, status.HTTP_403_FORBIDDEN)


class RepairNotAllowedError(BaseCustomException):
    def __init__(
        self, message: str = "Repair is not allowed in the current status"
    ) -> None:
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class RepairAlreadyCompletedError(BaseCustomException):
    def __init__(self, message: str = "Repair has already been submited") -> None:
        super().__init__(message, status.HTTP_409_CONFLICT)
