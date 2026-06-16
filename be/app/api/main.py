from fastapi import APIRouter
from app.api.routes import devices, users

api_router = APIRouter()
api_router.include_router(devices.router)
api_router.include_router(users.router)
