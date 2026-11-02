from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RepairCreate(BaseModel):
    complaint_id: int = Field(gt=0)
    issue_found: str = Field(min_length=5)
    repair_description: str = Field(min_length=5)
    remarks: str | None = None


class RepairUpdate(BaseModel):
    issue_found: str | None = Field(default=None, min_length=5)
    repair_description: str | None = Field(default=None, min_length=5)
    remarks: str | None = None


class RepairResponse(BaseModel):
    id: int
    complaint_id: int
    lineman_id: int
    issue_found: str
    repair_description: str
    repair_status: str
    repair_started_at: datetime
    repair_completed_at: datetime | None
    repair_image_path: str | None
    remarks: str | None
    model_config = ConfigDict(from_attributes=True)
