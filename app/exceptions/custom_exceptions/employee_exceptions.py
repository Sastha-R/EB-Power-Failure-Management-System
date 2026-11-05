from fastapi import status

from app.exceptions.custom_exceptions.base_exception import BaseCustomException


class EmployeeNotFoundError(BaseCustomException):
    def __init__(self, message: str = "Employee not found") -> None:
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class EmployeeAlreadyExistsError(BaseCustomException):
    def __init__(self, message: str = "Employee already exists") -> None:
        super().__init__(message, status.HTTP_409_CONFLICT)


class EmployeeAlreadyInactiveError(BaseCustomException):
    def __init__(self, message: str = "Employee is already inactive") -> None:
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class InvalidEmployeeRoleError(BaseCustomException):
    def __init__(self, message: str = "Invalid employee role") -> None:
        super().__init__(message, status.HTTP_400_BAD_REQUEST)
