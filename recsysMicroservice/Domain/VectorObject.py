from pydantic import BaseModel
from typing import List, Optional
from abc import ABC, abstractmethod


class VectorObject(BaseModel, ABC):
    id: int
    tfidf_descr_vector: Optional[List[float]]
    image_vector: Optional[List[float]]
    tags_vector: Optional[List[float]]
    bert_descr_vector: Optional[List[float]]

    @staticmethod
    @abstractmethod
    def collection_name() -> str:
        """Property that must be implemented by subclasses to return the collection name."""
        return NotImplemented
