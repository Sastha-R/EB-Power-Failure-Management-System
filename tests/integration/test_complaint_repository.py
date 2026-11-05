import pytest

from app.repositories.implementations.complaint_repository import ComplaintRepository
from app.repositories.implementations.customer_repository import CustomerRepository


@pytest.mark.integration
@pytest.mark.asyncio
async def test_complaint_repository_create_list_and_update(db_session):
    customer = await CustomerRepository().create_customer(
        db_session,
        {
            "customer_code": "CUSCMPINT01",
            "username": "complaint_integration",
            "email": "complaint.integration@example.com",
            "password": "hashed-password",
            "phone_number": "9876543210",
            "door_no": "12",
            "street": "Integration Road",
            "district": "Test District",
            "pincode": "600001",
        },
    )
    repository = ComplaintRepository()
    complaint = await repository.create_complaint(
        db_session,
        {
            "complaint_number": "CMPINT0001",
            "customer_id": customer.id,
            "door_no": "12",
            "street": "Integration Road",
            "district": "Test District",
            "pincode": "600001",
            "failure_type": "Power outage",
            "description": "Power has been unavailable for hours",
        },
    )

    customer_complaints = await repository.get_customer_complaints(
        db_session, customer.id
    )
    updated = await repository.update_complaint(
        db_session, complaint, {"description": "Power restored after repair"}
    )

    assert complaint.id in {item.id for item in customer_complaints}
    assert updated.description == "Power restored after repair"
