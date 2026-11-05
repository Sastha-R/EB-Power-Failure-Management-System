from app.repositories.implementations.repair_repository import RepairRepository
from app.repositories.implementations.complaint_repository import ComplaintRepository
from app.services.implementations.repair_service import RepairService


def get_repair_service() -> RepairService:
    repair_repository: RepairRepository = RepairRepository()
    complaint_repository: ComplaintRepository = ComplaintRepository()

    return RepairService(
        repair_repository,
        complaint_repository
    )
