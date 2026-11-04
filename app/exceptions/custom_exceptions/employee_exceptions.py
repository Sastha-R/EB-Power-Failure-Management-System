from fastapi import status

from app.exceptions.custom_exceptions.base_exception import BaseCustomException


class EmployeeNotFoundError(BaseCustomException):
    def __init__(self, message="Employee not found"):
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class EmployeeAlreadyExistsError(BaseCustomException):
    def __init__(self, message="Employee already exists"):
        super().__init__(message, status.HTTP_409_CONFLICT)


class EmployeeAlreadyInactiveError(BaseCustomException):
    def __init__(self, message="Employee is already inactive"):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class InvalidEmployeeRoleError(BaseCustomException):
    def __init__(self, message="Invalid employee role"):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)