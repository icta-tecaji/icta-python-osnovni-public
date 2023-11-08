from fastapi import APIRouter
from app.api.endpoints import ping, items, notes, parser

api_router = APIRouter()

api_router.include_router(ping.router, tags=["Test Endpoint"])
api_router.include_router(items.router, tags=["Items"], prefix="/items")
api_router.include_router(notes.router, tags=["Notes"], prefix="/notes")
api_router.include_router(parser.router, tags=["Parser"], prefix="/parser")
