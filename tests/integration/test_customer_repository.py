import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer
from app.repositories.implementations.customer_repository import CustomerRepository


@pytest.mark.integration
@pytest.mark.asyncio
async def test_customer_repository_create_lookup_and_deactivate(
    db_session: AsyncSession,
) -> None:
    repository: CustomerRepository = CustomerRepository()
    customer: Customer = await repository.create_customer(
        db_session,
        {
            "customer_code": "CUSINT0001",
            "username": "customer_integration",
            "email": "customers@example.com",
            "password": "hashed-password",
            "phone_number": "9876543210",
            "door_no": "11",
            "street": "Integration Road",
            "district": "Test District",
            "pincode": "600001",
        },
    )

    found: Customer | None = await repository.get_customer_by_email(
        db_session, customer.email
    )
    deactivated: Customer = await repository.deactivate_customer(db_session, customer)

    assert found is not None
    assert found.id == customer.id
    assert deactivated.is_active is False
