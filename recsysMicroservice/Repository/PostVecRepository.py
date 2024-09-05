from .VecRepository import VecRepository
from ..Domain.PostVec import PostVec


class PostVecRepository(VecRepository[PostVec]):

    def __init__(self):
        super().__init__(PostVec)
