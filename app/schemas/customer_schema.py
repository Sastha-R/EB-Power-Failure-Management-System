from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CustomerCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    phone_number: str = Field(pattern=r"^[6-9][0-9]{9}$")
    door_no: str = Field(max_length=20)
    street: str = Field(max_length=150)
    district: str = Field(max_length=100)
    pincode: str = Field(pattern=r"^[1-9][0-9]{5}$")


class CustomerResponse(BaseModel):
    id: int
    customer_code: str
    username: str
    email: EmailStr
    phone_number: str
    door_no: str
    street: str
    district: str
    pincode: str
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
