from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.exceptions.custom_exceptions.repair_exceptions import (
    RepairAlreadyCompletedError,
    RepairNotAssignedError,
)
from app.services.implementations.repair_service import RepairService


@pytest.mark.asyncio
@pytest.mark.unit
async def test_complete_repair_commits_and_updates_status(mock_repository):
    complaint = SimpleNamespace(status="ASSIGNED")
    repair = object()
    mock_repository.get_complaint_by_id.return_value = complaint
    mock_repository.get_assignment.return_value = object()
    mock_repository.get_repair_by_complaint_id.return_value = None
    mock_repository.create_repair.return_value = repair
    db = SimpleNamespace(commit=AsyncMock(), refresh=AsyncMock(), rollback=AsyncMock())
    result = await RepairService(mock_repository, mock_repository).complete_repair(
        db,
        4,
        2,
        SimpleNamespace(
            model_dump=lambda: {
                "issue_found": "bad wire",
                "repair_description": "replaced wire",
            }
        ),
    )
    assert result is repair and complaint.status == "REPAIR_COMPLETED"
    db.commit.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.unit
async def test_complete_repair_requires_assignment(mock_repository):
    mock_repository.get_complaint_by_id.return_value = SimpleNamespace(
        status="ASSIGNED"
    )
    mock_repository.get_assignment.return_value = None
    with pytest.raises(RepairNotAssignedError):
        await RepairService(mock_repository, mock_repository).complete_repair(
            None, 1, 2, None
        )


@pytest.mark.asyncio
@pytest.mark.unit
async def test_complete_repair_rejects_duplicate(mock_repository):
    mock_repository.get_complaint_by_id.return_value = SimpleNamespace(
        status="ASSIGNED"
    )
    mock_repository.get_assignment.return_value = object()
    mock_repository.get_repair_by_complaint_id.return_value = object()
    with pytest.raises(RepairAlreadyCompletedError):
        await RepairService(mock_repository, mock_repository).complete_repair(
            None, 1, 2, None
        )


@pytest.mark.asyncio
@pytest.mark.unit
async def test_upload_repair_image_delegates_to_storage(
    mock_repository, mock_external_operations
):
    complaint = SimpleNamespace(status="REPAIR_COMPLETED")
    repair = SimpleNamespace()
    mock_repository.get_complaint_by_id.return_value = complaint
    mock_repository.get_assignment.return_value = object()
    mock_repository.get_repair_by_complaint_id.return_value = repair
    mock_repository.update_repair_image.return_value = repair
    result = await RepairService(mock_repository, mock_repository).upload_repair_image(
        None, 1, 2, object()
    )
    assert result is repair
    mock_repository.update_repair_image.assert_awaited_once_with(
        None, repair, "/tmp/test-upload.png"
    )
