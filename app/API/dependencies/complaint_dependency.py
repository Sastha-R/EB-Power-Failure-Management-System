from app.repositories.implementations.complaint_repository import ComplaintRepository
from app.repositories.implementations.customer_repository import CustomerRepository
from app.repositories.implementations.employee_repository import EmployeeRepository
from app.services.implementations.complaint_service import ComplaintService


def get_complaint_service() -> ComplaintService:
    complaint_repository: ComplaintRepository = ComplaintRepository()
    employee_repository: EmployeeRepository = EmployeeRepository()
    customer_repository: CustomerRepository = CustomerRepository()

    return ComplaintService(
        complaint_repository,
        employee_repository,
        customer_repository,
    )
