from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession


class AuthServiceInterface(ABC):

    @abstractmethod
    async def employee_login(self, db: AsyncSession, email: str, password: str):
        pass

    @abstractmethod
    async def customer_login(self, db: AsyncSession, email: str, password: str):
        pass

    @abstractmethod
    async def refresh_access_token(self, db: AsyncSession, refresh_token: str):
        pass