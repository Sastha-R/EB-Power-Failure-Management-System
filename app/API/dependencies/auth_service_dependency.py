from app.repositories.implementations.employee_repository import EmployeeRepository
from app.repositories.implementations.customer_repository import CustomerRepository
from app.services.implementations.auth_service import AuthService


def get_auth_service() -> AuthService:
    employee_repository: EmployeeRepository = EmployeeRepository()
    customer_repository: CustomerRepository = CustomerRepository()

    return AuthService(
        employee_repository,
        customer_repository
    )
