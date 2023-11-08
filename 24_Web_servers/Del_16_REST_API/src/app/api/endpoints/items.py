from fastapi import APIRouter
from app.schemas import items

router = APIRouter()


@router.get("/")
async def get_items():
    return {"items": "sdsdsdsd"}


@router.get("/{item_id}")
async def get_item(item_id: int):
    return {"item": "sdsdsdsd", "id": item_id}


@router.post("/")
async def create_item(item: items.Item):
    print(item)
    print(item.name)
    return {"status": "ok"}
