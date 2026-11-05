from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class RepairServiceInterface(ABC):
    @abstractmethod
    async def complete_repair(
        self, db, complaint_id: int, lineman_id: int, repair_data
    ):
        pass

    @abstractmethod
    async def upload_repair_image(
        self, db: AsyncSession, complaint_id: int, lineman_id: int, image
    ):
        pass

    @abstractmethod
    async def get_all_repair_details(self, db: AsyncSession):
        pass

    # @abstractmethod
    # async def update_complaint(
    #     self,
    #     db: AsyncSession,
    #     complaint_id: int,
    #     customer_id: int,
    #     complaint_data,
    # ):
    #     pass

    