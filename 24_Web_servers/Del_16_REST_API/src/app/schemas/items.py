from pydantic import BaseModel
from typing import List


class Item(BaseModel):
    name: str = None
    description: str = None
    price: float = 0
    tags: List[str] = []
