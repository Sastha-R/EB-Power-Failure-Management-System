from app.repositories.implementations.complaint_repository import ComplaintRepository
from app.repositories.implementations.employee_repository import EmployeeRepository
from app.services.implementations.complaint_service import ComplaintService


def get_complaint_service():
    complaint_repository = ComplaintRepository()
    employee_repository = EmployeeRepository()

    return ComplaintService(
        complaint_repository,
        employee_repository
    )