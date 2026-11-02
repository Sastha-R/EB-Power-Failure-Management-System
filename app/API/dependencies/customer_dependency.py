from app.services.implementations.customer_service import CustomerService
from app.repositories.implementations.customer_repository import CustomerRepository


def get_customer_service():
    customer_repository = CustomerRepository()
    return CustomerService(customer_repository)