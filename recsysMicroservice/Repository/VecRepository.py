from abc import ABC
from pymilvus import MilvusClient, AnnSearchRequest, Collection, RRFRanker, connections
from ..Domain.VectorObject import VectorObject
from typing import List, Generic, TypeVar, Type

Entity = TypeVar("Entity", bound=VectorObject)


class VecRepository(ABC, Generic[Entity]):

    def __init__(self, entity_class: Type[Entity]):
        self._milvus_client = MilvusClient("http://localhost:19530")
        self.entity_class = entity_class
        self.__connection = connections.connect(
            alias="default", 
            host='localhost',
            port='19530'
        )
        self.__collection = Collection(self.entity_class.collection_name())
        self.__collection.load()
        self._milvus_client.load_collection(
                collection_name=self.entity_class.collection_name(),
                replica_number=1
        )



    def upsert(self, vector_object: Entity) -> None:
        collection_name = self.entity_class.collection_name()
        self._milvus_client.upsert(collection_name=collection_name, data=vector_object.model_dump())

    def find_by_id(self, id: int) -> Entity:
        collection_name = self.entity_class.collection_name()
        item = self._milvus_client.get(collection_name=collection_name, ids=[id])
        return self.entity_class(**item[0])

    def find_similar(self, vector_object: VectorObject, n: int) -> List[Entity]:

        reqs = []

        for vector in ["bert_descr_vector", "tfidf_descr_vector", "image_vector", "tags_vector"]:

            search_param_bert = {
                "data": [getattr(vector_object, vector)],
                "anns_field": vector,
                "param": {
                    "metric_type": "COSINE",
                    "params": {"nprobe": 10}
                },
                "limit": n
                }

            reqs.append(AnnSearchRequest(**search_param_bert))

        rerank = RRFRanker()

        res = self.__collection.hybrid_search(reqs, rerank, limit=n)

        similar_objects = []

        for hit in res[0]:
            vector_object = self.find_by_id(hit.id)
            similar_objects.append(vector_object)

        return similar_objects
