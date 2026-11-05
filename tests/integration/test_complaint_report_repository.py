import pytest

from app.repositories.implementations.complaint_report_repository import (
    ComplaintReportRepository,
)
from app.repositories.implementations.complaint_repository import ComplaintRepository
from app.repositories.implementations.customer_repository import CustomerRepository


@pytest.mark.integration
@pytest.mark.asyncio
async def test_complaint_report_repository_counts_each_status(db_session):
    customer = await CustomerRepository().create_customer(
        db_session,
        {
            "customer_code": "CUSREPORT001",
            "username": "report_customer",
            "email": "report.customer@example.com",
            "password": "hashed-password",
            "phone_number": "9876543210",
            "door_no": "20",
            "street": "Report Road",
            "district": "Test District",
            "pincode": "600001",
        },
    )
    complaint_repository = ComplaintRepository()
    for index, status in enumerate(
        ("PENDING", "ASSIGNED", "ASSIGNED", "REPAIR_COMPLETED", "CLOSED"),
        start=1,
    ):
        await complaint_repository.create_complaint(
            db_session,
            {
                "complaint_number": f"CMPREPORT{index:04d}",
                "customer_id": customer.id,
                "door_no": "20",
                "street": "Report Road",
                "district": "Test District",
                "pincode": "600001",
                "failure_type": "Power outage",
                "description": "Power has been unavailable for several hours",
                "status": status,
            },
        )

    statistics = await ComplaintReportRepository().get_complaint_statistics(db_session)

    assert statistics == {
        "total_complaints": 5,
        "pending": 1,
        "assigned": 2,
        "repair_completed": 1,
        "closed": 1,
    }


@pytest.mark.integration
@pytest.mark.asyncio
async def test_complaint_report_repository_returns_zero_for_empty_database(db_session):
    statistics = await ComplaintReportRepository().get_complaint_statistics(db_session)

    assert statistics == {
        "total_complaints": 0,
        "pending": 0,
        "assigned": 0,
        "repair_completed": 0,
        "closed": 0,
    }
