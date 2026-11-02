from fastapi import FastAPI
from app.API.routers.auth_router import auth_router
from app.API.routers.employee_router import employee_router



app = FastAPI(title="EB Power Failure Management System")

app.include_router(employee_router)
app.include_router(auth_router)