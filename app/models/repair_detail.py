from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class RepairDetail(Base):
    __tablename__ = "repair_details"

    id: Mapped[int] = mapped_column(primary_key=True)

    complaint_id: Mapped[int] = mapped_column(
        ForeignKey("complaints.id"), nullable=False
    )

    lineman_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)

    issue_found: Mapped[str] = mapped_column(Text, nullable=False)

    repair_description: Mapped[str] = mapped_column(Text, nullable=False)

    repair_status: Mapped[str] = mapped_column(
        String(30), nullable=False, default="IN_PROGRESS"
    )

    repair_started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    repair_completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    repair_image_path: Mapped[str | None] = mapped_column(String(255), nullable=True)

    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)
