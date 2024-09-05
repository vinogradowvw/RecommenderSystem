from .VectorObject import VectorObject


class PostVec(VectorObject):

    @staticmethod
    def collection_name() -> str:
        return 'post'
