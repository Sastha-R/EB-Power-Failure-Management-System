import pytest

from app.repositories.implementations.complaint_repository import ComplaintRepository
from app.repositories.implementations.customer_repository import CustomerRepository
from app.repositories.implementations.employee_repository import EmployeeRepository


@pytest.mark.integration
@pytest.mark.asyncio
async def test_assignment_repository_create_and_list_by_lineman(db_session):
    customer = await CustomerRepository().create_customer(
        db_session,
        {
            "customer_code": "CUSASNINT01",
            "username": "assignment_customer",
            "email": "assignment.customer@example.com",
            "password": "hashed-password",
            "phone_number": "9876543210",
            "door_no": "13",
            "street": "Integration Road",
            "district": "Test District",
            "pincode": "600001",
        },
    )
    employee_repository = EmployeeRepository()
    lineman = await employee_repository.create_employee(
        db_session,
        {
            "employee_code": "EMPASNINT01",
            "username": "assignment_lineman",
            "email": "assignment.lineman@example.com",
            "password": "hashed-password",
            "role": "lineman",
            "phone_number": "9876543211",
            "door_no": "14",
            "street": "Integration Road",
            "district": "Test District",
            "pincode": "600001",
        },
    )
    admin = await employee_repository.create_employee(
        db_session,
        {
            "employee_code": "EMPASNINT02",
            "username": "assignment_admin",
            "email": "assignment.admin@example.com",
            "password": "hashed-password",
            "role": "admin",
            "phone_number": "9876543212",
            "door_no": "15",
            "street": "Integration Road",
            "district": "Test District",
            "pincode": "600001",
        },
    )
    complaint_repository = ComplaintRepository()
    complaint = await complaint_repository.create_complaint(
        db_session,
        {
            "complaint_number": "CMPASNINT01",
            "customer_id": customer.id,
            "door_no": "13",
            "street": "Integration Road",
            "district": "Test District",
            "pincode": "600001",
            "failure_type": "Power outage",
            "description": "Power has been unavailable for hours",
        },
    )

    assignment = await complaint_repository.assign_complaint(
        db_session,
        {
            "complaint_id": complaint.id,
            "lineman_id": lineman.id,
            "assigned_by": admin.id,
            "remarks": "Please inspect the local line",
        },
    )
    assigned = await complaint_repository.get_assigned_complaints(
        db_session, lineman.id
    )

    assert assignment.complaint_id == complaint.id
    assert complaint.id in {item.id for item in assigned}
