from fastapi import status


class BaseCustomException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> None:
        self.message: str = message
        self.status_code: int = status_code
        super().__init__(message)
