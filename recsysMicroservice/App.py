from fastapi import FastAPI
from .Controller import PostController, UserController

app = FastAPI()

app.include_router(PostController.router)
app.include_router(UserController.router)
