from fastapi import APIRouter, Depends
from typing import List
from ..Domain.PostDTO import PostDTO
from ..Service.PostService import PostService
from ..Dependencies import get_post_service

router = APIRouter(prefix="/post")


@router.get("/recommendations/post/{post_id}", response_model=List[int])
async def get_recommendations_by_post(
    post_id: int,
    limit: int,
    post_service: PostService = Depends(get_post_service)
):
    post_ids = post_service.get_recommended_posts_by_post_id(post_id, limit)
    return post_ids


@router.get("/recommendations/user/{user_id}", response_model=List[int])
async def get_recommendations_by_user(
    user_id: int,
    limit: int,
    post_service: PostService = Depends(get_post_service)
):
    post_ids = post_service.get_recommended_posts_by_user_id(user_id, limit)
    return post_ids


@router.post("/save")
async def save_post(
    post: PostDTO,
    post_service: PostService = Depends(get_post_service)
):
    post_service.upsert(post)
    return {"message": "Post upserted successfully"}
