from fastapi import FastAPI

from recsysMicroservice.Kafka.Consumer import KafkaConsumer
from .Controller import PostController, UserController

consumer = KafkaConsumer()

app = FastAPI()

app.include_router(PostController.router)
app.include_router(UserController.router)
