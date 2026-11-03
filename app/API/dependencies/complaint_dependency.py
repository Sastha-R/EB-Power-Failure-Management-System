from app.repositories.implementations.complaint_repository import ComplaintRepository
from app.services.implementations.complaint_service import ComplaintService


def get_complaint_service():
    complaint_repository = ComplaintRepository()

    return ComplaintService(complaint_repository)