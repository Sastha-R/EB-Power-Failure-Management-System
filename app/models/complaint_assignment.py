from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class ComplaintAssignment(Base):
    __tablename__ = "complaint_assignments"

    id: Mapped[int] = mapped_column(primary_key=True)

    complaint_id: Mapped[int] = mapped_column(
        ForeignKey("complaints.id"), nullable=False
    )

    lineman_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)

    assigned_by: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)
