from app.api.endpoints import auth, ping, user
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(ping.router, tags=["Test"])
api_router.include_router(auth.router, tags=["Auth"], prefix="/auth")
api_router.include_router(user.router, tags=["User"], prefix="/user")
