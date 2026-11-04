from fastapi import status

from app.exceptions.custom_exceptions.base_exception import (
    BaseCustomException,
)


class CustomerNotFoundError(BaseCustomException):
    def __init__(self, message="Customer not found"):
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class CustomerAlreadyExistsError(BaseCustomException):
    def __init__(self, message="Customer already exists"):
        super().__init__(message, status.HTTP_409_CONFLICT)


class CustomerAlreadyInactiveError(BaseCustomException):
    def __init__(self, message="Customer is already inactive"):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)