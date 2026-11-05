from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class ComplaintReportRepositoryInterface(ABC):
    @abstractmethod
    async def get_complaint_statistics(self, db: AsyncSession) -> dict[str, int]:
        pass
