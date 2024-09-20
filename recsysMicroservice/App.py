from fastapi import FastAPI
from .Controller import PostController, UserController
from .milvus_setup import setup


app = FastAPI()

app.include_router(PostController.router)
app.include_router(UserController.router)
