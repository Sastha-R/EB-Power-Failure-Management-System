from app.repositories.implementations.customer_repository import CustomerRepository
from app.services.implementations.customer_service import CustomerService


def get_customer_service() -> CustomerService:
    customer_repository: CustomerRepository = CustomerRepository()
    return CustomerService(customer_repository)
