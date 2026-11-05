from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile

from app.models.repair_detail import RepairDetail
from app.schemas.repair_schema import RepairCreate


class RepairServiceInterface(ABC):
    @abstractmethod
    async def complete_repair(
        self,
        db: AsyncSession,
        complaint_id: int,
        lineman_id: int,
        repair_data: RepairCreate,
    ) -> RepairDetail:
        pass

    @abstractmethod
    async def upload_repair_image(
        self,
        db: AsyncSession,
        complaint_id: int,
        lineman_id: int,
        image: UploadFile,
    ) -> RepairDetail:
        pass

    @abstractmethod
    async def get_all_repair_details(self, db: AsyncSession) -> list[RepairDetail]:
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

    
