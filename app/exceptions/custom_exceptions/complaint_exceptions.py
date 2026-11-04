from fastapi import status

from app.exceptions.custom_exceptions.base_exception import (
    BaseCustomException,
)


class ComplaintNotFoundError(BaseCustomException):
    def __init__(self, message="Complaint not found"):
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class ComplaintAlreadyExistsError(BaseCustomException):
    def __init__(self, message="Complaint already exists"):
        super().__init__(message, status.HTTP_409_CONFLICT)


class ComplaintAlreadyAssignedError(BaseCustomException):
    def __init__(self, message="Complaint is already assigned"):
        super().__init__(message, status.HTTP_409_CONFLICT)


class ComplaintNotEditableError(BaseCustomException):
    def __init__(self, message="Complaint cannot be edited"):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class ComplaintNotReadyToCloseError(BaseCustomException):
    def __init__(self, message="Complaint is not ready to close"):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class UnauthorizedComplaintAccessError(BaseCustomException):
    def __init__(self, message="You are not authorized to access this complaint"):
        super().__init__(message, status.HTTP_403_FORBIDDEN)