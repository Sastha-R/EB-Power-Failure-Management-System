from app.schemas.assignment_schema import AssignmentCreate, AssignmentResponse
from app.schemas.auth_schema import (
    LoginRequest,
    MessageResponse,
    RefreshTokenRequest,
    TokenResponse,
)
from app.schemas.complaint_schema import (
    ComplaintCreate,
    ComplaintResponse,
    ComplaintUpdate,
)
from app.schemas.customer_schema import CustomerCreate, CustomerResponse
from app.schemas.employee_schema import EmployeeCreate, EmployeeResponse
from app.schemas.repair_schema import RepairCreate, RepairResponse

__all__: list[str] = [
    "AssignmentCreate",
    "AssignmentResponse",
    "ComplaintCreate",
    "ComplaintResponse",
    "ComplaintUpdate",
    "CustomerCreate",
    "CustomerResponse",
    "EmployeeCreate",
    "EmployeeResponse",
    "LoginRequest",
    "MessageResponse",
    "RefreshTokenRequest",
    "RepairCreate",
    "RepairResponse",
    "TokenResponse",
]
