from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession


class AuthServiceInterface(ABC):

    @abstractmethod
    async def employee_login(self, db: AsyncSession, email: str, password: str):
        pass

    