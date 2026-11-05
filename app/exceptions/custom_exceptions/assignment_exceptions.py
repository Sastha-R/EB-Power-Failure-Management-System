from fastapi import status

from app.exceptions.custom_exceptions.base_exception import (
    BaseCustomException,
)


class AssignmentNotFoundError(BaseCustomException):
    def __init__(self, message: str = "Assignment not found") -> None:
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class AssignmentAlreadyExistsError(BaseCustomException):
    def __init__(self, message: str = "Assignment already exists") -> None:
        super().__init__(message, status.HTTP_409_CONFLICT)


class InvalidLinemanAssignmentError(BaseCustomException):
    def __init__(self, message: str = "Invalid lineman assignment") -> None:
        super().__init__(message, status.HTTP_400_BAD_REQUEST)
