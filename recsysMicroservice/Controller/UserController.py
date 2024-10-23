from fastapi import APIRouter, Depends
from ..Service.UserService import UserService
from ..Dependencies import get_user_service


router = APIRouter(prefix="/user")


@router.post("/like/user/{user_id}/post/{post_id}")
async def user_liked(user_id: int, post_id: int, user_service: UserService = Depends(get_user_service)):
    user_service.update_users_vector(user_id=user_id, post_id=post_id, weight=30)


@router.post("/like/user/{user_id}/post/{post_id}")
async def user_purchased(user_id: int, post_id: int, user_service: UserService = Depends(get_user_service)):
    user_service.update_users_vector(user_id=user_id, post_id=post_id, weight=70)


@router.post("/init/{user_id}")
async def init_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    user_service.init(user_id=user_id)


@router.delete("/{id}")
async def delete_by_id(id: int, user_service: UserService = Depends(get_user_service)):
    user_service.delete_by_id(id)
