from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.complaint_assignment import ComplaintAssignment
from app.models.repair_detail import RepairDetail


class RepairRepositoryInterface(ABC):

    @abstractmethod
    async def get_assignment(
        self, db: AsyncSession, complaint_id: int, lineman_id: int
    ) -> ComplaintAssignment | None:
        pass

    @abstractmethod
    async def get_repair_by_complaint_id(
        self, db: AsyncSession, complaint_id: int
    ) -> RepairDetail | None:
        pass

    @abstractmethod
    async def create_repair(
        self, db: AsyncSession, repair_data: dict[str, object]
    ) -> RepairDetail:
        pass

    @abstractmethod
    async def update_repair_image(
        self, db: AsyncSession, repair: RepairDetail, image_path: str
    ) -> RepairDetail:
        pass
