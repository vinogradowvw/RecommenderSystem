from io import BytesIO
from typing import List
import requests
from PIL import Image

from injector import inject
from ..Domain.PostDTO import PostDTO
from ..Domain.PostVec import PostVec
from ..Repository.PostVecRepository import PostVecRepository
from ..Repository.UserVecRepository import UserVecRepository
import numpy as np

from .Vectorizers.ImageVectorizer import ImageVectorizer
from .Vectorizers.TextVectorizer import TextVectorizer


class PostService:

    @inject
    def __init__(self, post_vec_repo: PostVecRepository, user_vec_repo: UserVecRepository,
                 text_vectorizer: TextVectorizer, image_vectorizer: ImageVectorizer):
        self.__post_vec_repo = post_vec_repo
        self.__user_vec_repo = user_vec_repo
        self.__text_vectorizer = text_vectorizer
        self.__image_vectorizer = image_vectorizer

    def get_recommended_posts_by_user_id(self, user_id: int, n: int) -> List[int]:
        user = self.__user_vec_repo.find_by_id(user_id)
        posts = self.__post_vec_repo.find_similar(user, n)
        post_ids = [post.id for post in posts]
        return post_ids

    def get_recommended_posts_by_post_id(self, post_id: int, n: int) -> List[int]:
        post = self.__post_vec_repo.find_by_id(post_id)
        posts = self.__post_vec_repo.find_similar(post, n)
        post_ids = [post.id for post in posts]
        return post_ids

    def upsert(self, post: PostDTO) -> None:

        tags_vector = self.__text_vectorizer.bow_vectorize(post.tags)

        tfidf_descr_vector = self.__text_vectorizer.tfidf_vectorize(post.description)
        bert_descr_vector = self.__text_vectorizer.bert_vectorize(post.description)

        image_vectors = []
        for image in post.images:
            response = requests.get("http://localhost:8080/image/{}".format(image))

            with Image.open(BytesIO(response.content)) as im:
                image_vectors.append(self.__image_vectorizer.resnet_vectorize(im))

        image_vector = np.mean(image_vectors, axis=0)

        post_vec = PostVec(id=post.id,
                           bert_descr_vector=bert_descr_vector.tolist(),
                           tfidf_descr_vector=tfidf_descr_vector.tolist(),
                           tags_vector=tags_vector.tolist(),
                           image_vector=image_vector.tolist())

        self.__post_vec_repo.upsert(post_vec)
