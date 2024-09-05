from typing import List

import numpy as np

from injector import inject

from ..Domain.UserVec import UserVec
from ..Repository.PostVecRepository import PostVecRepository
from ..Repository.UserVecRepository import UserVecRepository


class UserService:

    @inject
    def __init__(self, user_vec_repo: UserVecRepository, post_vec_repo: PostVecRepository):
        self.__user_vec_repo = user_vec_repo
        self.__post_vec_repo = post_vec_repo

    def get_recommended_users_by_user_id(self, user_id: int, n: int) -> List[int]:
        user = self.__user_vec_repo.find_by_id(user_id)
        users = self.__user_vec_repo.find_similar(user, n)
        user_ids = [user.id for user in users]
        return user_ids

    def update_users_vector(self, user_id: int, post_id: int, weight: int):

        post = self.__post_vec_repo.find_by_id(post_id)
        old_user = self.__user_vec_repo.find_by_id(user_id)
        new_user = UserVec(id=user_id, weight_count=old_user.weight_count)

        for vector in ["bert_descr_vector", "tfidf_descr_vector", "image_vector", "tags_vector"]:

            post_vector = np.array(getattr(post, vector))
            old_user_vector = np.array(getattr(old_user, vector))

            new_user_vector = (old_user_vector * old_user.weight_count + weight * post_vector) / \
                          (old_user.weight_count + weight)

            setattr(new_user, vector, new_user_vector)

        new_user.weight_count = old_user.weight_count + weight

        self.__user_vec_repo.upsert(new_user)
