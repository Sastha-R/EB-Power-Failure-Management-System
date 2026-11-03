from abc import ABC, abstractmethod


class RepairServiceInterface(ABC):

    @abstractmethod
    async def complete_repair(
        self,
        db,
        complaint_id: int,
        lineman_id: int,
        repair_data
    ):
        pass

    @abstractmethod
    async def upload_repair_image(
        self, db, complaint_id: int, lineman_id: int, image
    ):
        pass