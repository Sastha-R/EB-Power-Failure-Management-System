from fastapi import FastAPI

from app.api.routers.auth_router import auth_router
from app.api.routers.customer_router import customer_router
from app.api.routers.employee_router import employee_router

app = FastAPI(title="EB Power Failure Management System")

app.include_router(employee_router)
app.include_router(auth_router)
app.include_router(customer_router)
