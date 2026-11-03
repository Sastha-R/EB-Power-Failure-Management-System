from app.repositories.implementations.employee_repository import EmployeeRepository
from app.repositories.implementations.customer_repository import CustomerRepository
from app.services.implementations.auth_service import AuthService


def get_auth_service():
    employee_repository = EmployeeRepository()
    customer_repository = CustomerRepository()

    return AuthService(
        employee_repository,
        customer_repository
    )