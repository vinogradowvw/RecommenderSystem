from recsysMicroservice import milvus_setup
from .Service.PostService import PostService
from .Service.UserService import UserService
from .Repository.PostVecRepository import PostVecRepository
from .Repository.UserVecRepository import UserVecRepository
from .Service.Vectorizers.ImageVectorizer import ImageVectorizer
from .Service.Vectorizers.TextVectorizer import TextVectorizer
from .milvus_setup import setup

setup()

user_repository = UserVecRepository()
post_repository = PostVecRepository()

image_vectorizer = ImageVectorizer()
text_vectorizer = TextVectorizer()

post_service = PostService(post_vec_repo=post_repository, user_vec_repo=user_repository, image_vectorizer=image_vectorizer, text_vectorizer=text_vectorizer)
user_service = UserService(user_vec_repo=user_repository, post_vec_repo=post_repository)


def get_post_service():
    return post_service


def get_user_service():
    return user_service
