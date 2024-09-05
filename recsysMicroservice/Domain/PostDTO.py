from typing import List

from pydantic import BaseModel


class PostDTO(BaseModel):
    id: int
    name: str
    description: str
    product: int
    user: int
    liked_users: List[int]
    tags: List[int]
    images: List[int]
