from typing import List

import numpy as np

# from injector import inject

from ..Domain.UserVec import UserVec
from ..Repository.PostVecRepository import PostVecRepository
from ..Repository.UserVecRepository import UserVecRepository


class UserService:

    # @inject
    def __init__(self, user_vec_repo: UserVecRepository, post_vec_repo: PostVecRepository):
        self.__user_vec_repo = user_vec_repo
        self.__post_vec_repo = post_vec_repo

    def get_recommended_users_by_user_id(self, user_id: int, limit: int) -> List[int]:
        user = self.__user_vec_repo.find_by_id(user_id)
        users = self.__user_vec_repo.find_similar(user, limit)
        user_ids = [user.id for user in users]
        return user_ids

    def update_users_vector(self, user_id: int, post_id: int, weight: int):

        post = self.__post_vec_repo.find_by_id(post_id)
        old_user = self.__user_vec_repo.find_by_id(user_id)
        new_user = UserVec(
            id=user_id,
            weight_count=old_user.weight_count,
            bert_descr_vector=old_user.bert_descr_vector,
            tfidf_descr_vector=old_user.tfidf_descr_vector,
            image_vector=old_user.image_vector,
            tags_vector=old_user.tags_vector,
        )

        for vector in ["bert_descr_vector", "tfidf_descr_vector", "image_vector", "tags_vector"]:

            post_vector = np.array(getattr(post, vector))
            old_user_vector = np.array(getattr(old_user, vector))

            new_user_vector = (old_user_vector * old_user.weight_count + weight * post_vector) / \
                          (old_user.weight_count + weight)

            setattr(new_user, vector, new_user_vector.tolist())

        new_user.weight_count = old_user.weight_count + weight

        self.__user_vec_repo.upsert(new_user)

    def delete_by_id(self, id: int):
        self.__user_vec_repo.delete_by_id(id)

    def init(self, user_id: int):
        dimentions = {}

        for field in self.__user_vec_repo.schema.fields:
            if (field.params):
                dimentions[field.name] = field.params['dim']

        user = UserVec(
            id=user_id,
            bert_descr_vector=[0]*dimentions['bert_descr_vector'],
            tfidf_descr_vector=[0]*dimentions['tfidf_descr_vector'],
            image_vector=[0]*dimentions['image_vector'],
            tags_vector=[0]*dimentions['tags_vector'],
            weight_count=0,
        )

        self.__user_vec_repo.upsert(user)
