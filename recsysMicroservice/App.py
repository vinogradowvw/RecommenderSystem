from fastapi import FastAPI
from .Kafka.Consumer import KafkaConsumer
from .Controller import PostController, UserController, AdministrationULSUTest

app = FastAPI()

app.include_router(PostController.router)
app.include_router(UserController.router)
app.include_router(AdministrationULSUTest.router)

# consumer = KafkaConsumer()
