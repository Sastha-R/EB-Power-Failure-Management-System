from app.repositories.implementations.employee_repository import EmployeeRepository
from app.services.implementations.auth_service import AuthService


def get_auth_service():
    employee_repository = EmployeeRepository()
    return AuthService(employee_repository)