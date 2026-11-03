from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AssignmentCreate(BaseModel):
    complaint_id: int = Field(gt=0)
    lineman_id: int = Field(gt=0)
    remarks: str | None = None


class AssignmentResponse(BaseModel):
    id: int
    complaint_id: int
    lineman_id: int
    assigned_by: int
    assigned_at: datetime
    remarks: str | None
    model_config = ConfigDict(from_attributes=True)


