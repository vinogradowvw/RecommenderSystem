from recsysMicroservice.Kafka.Producer import KafkaProducer
from recsysMicroservice.Service.PostService import PostService
from recsysMicroservice.Service.UserService import UserService
from recsysMicroservice.Repository.PostVecRepository import PostVecRepository
from recsysMicroservice.Repository.UserVecRepository import UserVecRepository
from recsysMicroservice.Service.Vectorizers.ImageVectorizer import ImageVectorizer
from recsysMicroservice.Service.Vectorizers.TextVectorizer import TextVectorizer
from recsysMicroservice.milvus_setup import setup

setup()

user_repository = UserVecRepository()
post_repository = PostVecRepository()

image_vectorizer = ImageVectorizer()
text_vectorizer = TextVectorizer()

post_service = PostService(post_vec_repo=post_repository, user_vec_repo=user_repository, image_vectorizer=image_vectorizer, text_vectorizer=text_vectorizer)
user_service = UserService(user_vec_repo=user_repository, post_vec_repo=post_repository)

producer = KafkaProducer()


def get_post_service():
    return post_service


def get_user_service():
    return user_service


def get_kafka_producer():
    return producer
