from fastapi import status

from app.exceptions.custom_exceptions.base_exception import (
    BaseCustomException,
)


class ComplaintNotFoundError(BaseCustomException):
    def __init__(self, message: str = "Complaint not found") -> None:
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class ComplaintAlreadyExistsError(BaseCustomException):
    def __init__(self, message: str = "Complaint already exists") -> None:
        super().__init__(message, status.HTTP_409_CONFLICT)


class ComplaintAlreadyAssignedError(BaseCustomException):
    def __init__(self, message: str = "Complaint is already assigned") -> None:
        super().__init__(message, status.HTTP_409_CONFLICT)


class ComplaintNotEditableError(BaseCustomException):
    def __init__(self, message: str = "Complaint cannot be edited") -> None:
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class ComplaintNotReadyToCloseError(BaseCustomException):
    def __init__(self, message: str = "Complaint is not ready to close") -> None:
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class UnauthorizedComplaintAccessError(BaseCustomException):
    def __init__(
        self, message: str = "You are not authorized to access this complaint"
    ) -> None:
        super().__init__(message, status.HTTP_403_FORBIDDEN)
