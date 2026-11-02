from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ComplaintCreate(BaseModel):
    door_no: str = Field(max_length=20)
    street: str = Field(max_length=150)
    district: str = Field(max_length=100)
    pincode: str = Field(pattern=r"^[1-9][0-9]{5}$")
    failure_type: str = Field(max_length=100)
    description: str = Field(min_length=10)


class ComplaintUpdate(BaseModel):
    door_no: str | None = Field(default=None, max_length=20)
    street: str | None = Field(default=None, max_length=150)
    district: str | None = Field(default=None, max_length=100)
    pincode: str | None = Field(default=None, pattern=r"^[1-9][0-9]{5}$")
    failure_type: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, min_length=10)


class ComplaintResponse(BaseModel):
    id: int
    complaint_number: str
    customer_id: int
    door_no: str
    street: str
    district: str
    pincode: str
    failure_type: str
    description: str
    priority: str
    status: str
    image_path: str | None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
