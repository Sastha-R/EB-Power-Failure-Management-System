from pydantic import BaseModel


class ComplaintStatisticsResponse(BaseModel):
    total_complaints: int
    pending: int
    assigned: int
    repair_completed: int
    closed: int
