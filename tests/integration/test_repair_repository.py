import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.complaint import Complaint
from app.models.customer import Customer
from app.models.employee import Employee
from app.models.repair_detail import RepairDetail
from app.repositories.implementations.complaint_repository import ComplaintRepository
from app.repositories.implementations.customer_repository import CustomerRepository
from app.repositories.implementations.employee_repository import EmployeeRepository
from app.repositories.implementations.repair_repository import RepairRepository


@pytest.mark.integration
@pytest.mark.asyncio
async def test_repair_repository_create_and_lookup(
    db_session: AsyncSession,
) -> None:
    customer: Customer = await CustomerRepository().create_customer(
        db_session,
        {
            "customer_code": "CUSREPINT01",
            "username": "repair_customer",
            "email": "repair.customer@example.com",
            "password": "hashed-password",
            "phone_number": "9876543210",
            "door_no": "16",
            "street": "Integration Road",
            "district": "Test District",
            "pincode": "600001",
        },
    )
    lineman: Employee = await EmployeeRepository().create_employee(
        db_session,
        {
            "employee_code": "EMPREPINT01",
            "username": "repair_lineman",
            "email": "repair.lineman@example.com",
            "password": "hashed-password",
            "role": "lineman",
            "phone_number": "9876543211",
            "door_no": "17",
            "street": "Integration Road",
            "district": "Test District",
            "pincode": "600001",
        },
    )
    complaint: Complaint = await ComplaintRepository().create_complaint(
        db_session,
        {
            "complaint_number": "CMPREPINT01",
            "customer_id": customer.id,
            "door_no": "16",
            "street": "Integration Road",
            "district": "Test District",
            "pincode": "600001",
            "failure_type": "Power outage",
            "description": "Power has been unavailable for hours",
        },
    )
    repository: RepairRepository = RepairRepository()
    repair: RepairDetail = await repository.create_repair(
        db_session,
        {
            "complaint_id": complaint.id,
            "lineman_id": lineman.id,
            "issue_found": "Damaged electrical cable",
            "repair_description": "Replaced the damaged cable",
        },
    )
    await db_session.commit()

    found: RepairDetail | None = await repository.get_repair_by_complaint_id(
        db_session, complaint.id
    )

    assert found is not None
    assert found.id == repair.id
