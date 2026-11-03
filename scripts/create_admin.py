import asyncio
import uuid

from sqlalchemy import select

from app.database.database import SessionLocal
from app.models import Employee
from app.core.security import hash_password


# Admin details
ADMIN_USERNAME = "admin"
ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "admin@123"

ADMIN_PHONE = "9876543210"
ADMIN_DOOR_NO = "10"
ADMIN_STREET = "Nehru nagar"
ADMIN_DISTRICT = "Coimbatore"
ADMIN_PINCODE = "641001"


async def create_admin():
    async with SessionLocal() as db:

        result = await db.execute(
            select(Employee).where(
                (Employee.email == ADMIN_EMAIL) |
                (Employee.username == ADMIN_USERNAME)
            )
        )

        if result.scalar_one_or_none():
            print("Admin already exists.")
            return

        admin = Employee(
            employee_code=f"EMP{uuid.uuid4().hex[:8].upper()}",
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            password=hash_password(ADMIN_PASSWORD),
            role="admin",
            phone_number=ADMIN_PHONE,
            door_no=ADMIN_DOOR_NO,
            street=ADMIN_STREET,
            district=ADMIN_DISTRICT,
            pincode=ADMIN_PINCODE,
            is_active=True
        )

        db.add(admin)
        await db.commit()
        

        print("Admin created successfully.")


if __name__ == "__main__":
    asyncio.run(create_admin())

