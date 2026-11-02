from app.repositories.implementations.employee_repository import EmployeeRepository
from app.services.implementations.employee_service import EmployeeService


def get_employee_service():

    employee_repository = EmployeeRepository()

    return EmployeeService(employee_repository)