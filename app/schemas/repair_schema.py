from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RepairCreate(BaseModel):
    issue_found: str = Field(min_length=5)
    repair_description: str = Field(min_length=5)
    remarks: str | None = None


class RepairResponse(BaseModel):
    id: int
    complaint_id: int
    lineman_id: int
    issue_found: str
    repair_description: str
    repair_completed_at: datetime
    repair_image_path: str | None
    remarks: str | None

    model_config = ConfigDict(from_attributes=True)
