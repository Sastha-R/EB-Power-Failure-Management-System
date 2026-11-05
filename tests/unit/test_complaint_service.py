from types import SimpleNamespace
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.exceptions.custom_exceptions.complaint_exceptions import (
    ComplaintNotEditableError,
    ComplaintNotFoundError,
)
from app.services.implementations.complaint_service import ComplaintService


@pytest.mark.asyncio
@pytest.mark.unit
async def test_create_complaint_sends_registered_email(
    mock_external_operations: dict[str, MagicMock | AsyncMock],
) -> None:
    complaint_repo: SimpleNamespace = SimpleNamespace(
        create_complaint=AsyncMock(
            return_value=SimpleNamespace(complaint_number="CMP1")
        )
    )
    customer_repo: SimpleNamespace = SimpleNamespace(
        get_customer_by_id=AsyncMock(
            return_value=SimpleNamespace(email="c@example.com")
        )
    )
    service: ComplaintService = ComplaintService(complaint_repo, None, customer_repo)
    result: SimpleNamespace = await service.create_complaint(
        None, 1, SimpleNamespace(model_dump=lambda: {"description": "outage here"})
    )
    assert result.complaint_number == "CMP1"
    mock_external_operations["email"].assert_called_once()


@pytest.mark.asyncio
@pytest.mark.unit
async def test_update_complaint_rejects_missing_record(
    mock_repository: MagicMock,
) -> None:
    mock_repository.get_complaint_by_id.return_value = None
    service: ComplaintService = ComplaintService(mock_repository, None, None)
    with pytest.raises(ComplaintNotFoundError):
        await service.update_complaint(None, 1, 2, None)


@pytest.mark.asyncio
@pytest.mark.unit
async def test_update_complaint_rejects_assigned_record(
    mock_repository: MagicMock,
) -> None:
    mock_repository.get_complaint_by_id.return_value = SimpleNamespace(
        customer_id=2, status="ASSIGNED"
    )
    with pytest.raises(ComplaintNotEditableError):
        await ComplaintService(mock_repository, None, None).update_complaint(
            None, 1, 2, None
        )


@pytest.mark.asyncio
@pytest.mark.unit
async def test_assign_complaint_rejects_non_pending(
    mock_repository: MagicMock,
) -> None:
    mock_repository.get_complaint_by_id.return_value = SimpleNamespace(status="CLOSED")
    with pytest.raises(HTTPException) as error:
        await ComplaintService(mock_repository, None, None).assign_complaint(
            None, 1, SimpleNamespace(complaint_id=2)
        )
    assert error.value.status_code == 400
