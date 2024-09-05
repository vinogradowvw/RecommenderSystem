from .VecRepository import VecRepository
from ..Domain.UserVec import UserVec


class UserVecRepository(VecRepository[UserVec]):

    def __init__(self):
        super().__init__(UserVec)
