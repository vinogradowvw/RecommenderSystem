from typing import List

from pydantic import BaseModel


class PostDTO(BaseModel):
    id: int
    name: str
    description: str
    tags: List[int]
    images: List[int]
