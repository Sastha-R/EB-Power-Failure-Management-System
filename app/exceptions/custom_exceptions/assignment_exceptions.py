from fastapi import status

from app.exceptions.custom_exceptions.base_exception import (
    BaseCustomException,
)


class AssignmentNotFoundError(BaseCustomException):
    def __init__(self, message="Assignment not found"):
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class AssignmentAlreadyExistsError(BaseCustomException):
    def __init__(self, message="Assignment already exists"):
        super().__init__(message, status.HTTP_409_CONFLICT)


class InvalidLinemanAssignmentError(BaseCustomException):
    def __init__(self, message="Invalid lineman assignment"):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)