from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id: Mapped[int] = mapped_column(primary_key=True)

    complaint_number: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )

    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)

    door_no: Mapped[str] = mapped_column(String(20), nullable=False)

    street: Mapped[str] = mapped_column(String(150), nullable=False)

    district: Mapped[str] = mapped_column(String(100), nullable=False)

    pincode: Mapped[str] = mapped_column(String(10), nullable=False)

    failure_type: Mapped[str] = mapped_column(String(100), nullable=False)

    description: Mapped[str] = mapped_column(Text, nullable=False)

    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="NORMAL")

    status: Mapped[str] = mapped_column(String(30), nullable=False, default="PENDING")

    image_path: Mapped[str | None] = mapped_column(String(250), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
