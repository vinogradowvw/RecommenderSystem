from fastapi import APIRouter

router = APIRouter(prefix='/test')


@router.get("hello", response_model=str)
async def hello():
    return "hello from recsys i am wirking on server"
