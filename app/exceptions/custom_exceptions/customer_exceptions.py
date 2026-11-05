from fastapi import status

from app.exceptions.custom_exceptions.base_exception import (
    BaseCustomException,
)


class CustomerNotFoundError(BaseCustomException):
    def __init__(self, message: str = "Customer not found") -> None:
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class CustomerAlreadyExistsError(BaseCustomException):
    def __init__(self, message: str = "Customer already exists") -> None:
        super().__init__(message, status.HTTP_409_CONFLICT)


class CustomerAlreadyInactiveError(BaseCustomException):
    def __init__(self, message: str = "Customer is already inactive") -> None:
        super().__init__(message, status.HTTP_400_BAD_REQUEST)
