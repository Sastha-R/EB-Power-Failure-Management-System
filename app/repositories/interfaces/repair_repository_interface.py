from abc import ABC, abstractmethod


class RepairRepositoryInterface(ABC):

    @abstractmethod
    async def get_assignment(self, db, complaint_id: int, lineman_id: int):
        pass

    @abstractmethod
    async def get_repair_by_complaint_id(self, db, complaint_id: int):
        pass

    @abstractmethod
    async def create_repair(self, db, repair_data: dict):
        pass

    @abstractmethod
    async def update_repair_image(self, db, repair, image_path: str):
        pass