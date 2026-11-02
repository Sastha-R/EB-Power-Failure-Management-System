from sqlalchemy import String, Boolean, DateTime, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base
from datetime import datetime

class Employee(Base):

    __tablename__ = "employees"

    __table_args__ = (
        CheckConstraint(
            "role IN ('admin', 'lineman')",
            name="check_employee_role"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    employee_code: Mapped[str] = mapped_column(
        String(50), 
        unique=True, 
        nullable=False
    )

    username: Mapped[str] = mapped_column(
        String(50), 
        unique=True, 
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(200), 
        unique=True, 
        nullable=False
    )

    password: Mapped[str] = mapped_column(
        String(250), 
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(20), 
        nullable=False
    )

    phone_number: Mapped[str] = mapped_column(
        String(15), 
        nullable=False
    )

    door_no: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    street: Mapped[str] = mapped_column(
        String(150), 
        nullable=False
    )

    district: Mapped[str] = mapped_column(
        String(100), 
        nullable=False
    )

    pincode: Mapped[str] = mapped_column(
        String(10), 
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, 
        default=True, 
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )