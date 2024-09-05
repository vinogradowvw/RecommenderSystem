from .VectorObject import VectorObject


class UserVec(VectorObject):

    weight_count: int

    @staticmethod
    def collection_name() -> str:
        return 'user'

    def __init__(self, **data):
        super().__init__(**data)
